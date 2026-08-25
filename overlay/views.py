"""Architecture views over an existing graph — the fork-only `view` verb.

`halal-graphify view <kind>` answers structural questions from
``graphify-out/graph.json`` with ZERO LLM tokens: every kind is a pure
function over the node-link JSON. The graph is built (and kept fresh, for
free) by ``extract``/``update``; this module only *presents* it.

Kinds
-----
map                  areas (= folders at an adaptive depth) and the
                     aggregated dependency edges between them
area <folder>        the files inside one folder, edges between them, and
                     "ports" (aggregated edges to other areas)
file <path>          the symbols in one file, intra-file edges, external
                     in/out edges grouped by area
node <name>          one symbol's neighbourhood: uses / used-by, by relation
impact <name>        everything that transitively depends on a symbol,
                     in rings by distance, grouped by area
trace <A> <B>        shortest dependency path A -> B (directed, then an
                     undirected fallback, flagged as such)
trace --from <X>     forward reachability from an entry point, by depth
flaws                cycles (area- and file-level SCCs), hub overload
                     (fan-in/fan-out above max(20, p95)), orphans (no
                     inbound dependency edges, entry points excluded)
stats                counts, the chosen area depth, staleness vs git HEAD

Every kind takes ``--json`` (machine form, consumed by the visual-reply
plugin) and prints a short text form otherwise.

Design constraints, deliberate:

* Hierarchy edges (``contains``, ``method``, ``defines``) build the
  folder/file/symbol tree. EVERY other relation (``calls``, ``imports``,
  ``references``, ``inherits``, ``case_of``, ``implements``, and whatever a
  future extractor adds) counts as a dependency edge. An explicit dependency
  list would silently drop new relations; an explicit hierarchy list only
  mis-classifies if upstream adds a new *structural* relation, which is far
  rarer and loudly visible in `stats`.
* ``INFERRED``/``AMBIGUOUS`` edges are included but carried with their
  confidence; ``--extracted-only`` drops them.
* Views default to ``file_type == "code"`` nodes: the map is an architecture
  view, and a documentation-heavy repo would otherwise drown it in prose
  sections (BroMic: 487 of 1,394 nodes are document sections).
  ``--all-types`` lifts the filter. ``node``/``impact``/``trace`` resolve
  names against ALL nodes — if the user names a doc section, answer about it.
* Flaw output is phrased as "look here", never as a verdict: an AST graph
  misses dynamic dispatch, reflection and config-driven wiring.
* Windows paths are normalised to forward slashes on load; node ids are
  never rewritten.

Exit codes: 0 ok · 1 error (bad input, unknown name, unreadable graph) ·
2 ambiguous name (candidates listed) · 3 no graph found (with the free
``extract --code-only`` offer).
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HIERARCHY_RELATIONS = frozenset({"contains", "method", "defines"})

ROOT_AREA = "(root)"          # files sitting directly in the project root
EXTERNAL_AREA = "(external)"  # nodes with no source_file (stdlib/framework symbols)

AREA_BAND = (5, 15)   # the map aims for this many areas
MAX_AUTO_DEPTH = 6    # deeper than this and it is not an architecture view


def _norm(p: str) -> str:
    """Forward slashes, no leading/trailing slash. Ids are never normalised."""
    return str(p or "").replace("\\", "/").strip("/")


# ---------------------------------------------------------------------------
# Graph loading and indexing
# ---------------------------------------------------------------------------

def find_graph(project: str, graph: str | None) -> Path | None:
    """Locate graph.json: explicit --graph, else <project>[/../..]/<out>/graph.json.

    Honours the GRAPHIFY_OUT env var the same way the rest of the package
    does. Walks upward so the verb works from a subdirectory, like git.
    """
    if graph:
        p = Path(graph)
        return p if p.is_file() else None
    out_name = os.environ.get("GRAPHIFY_OUT", "graphify-out")
    start = Path(project).resolve()
    if start.is_file():
        start = start.parent
    # `view map graphify-out` / `--project <out-dir>` should also just work.
    candidates = [start / "graph.json"] if start.name == Path(out_name).name else []
    for d in [start, *start.parents]:
        candidates.append(d / out_name / "graph.json")
    for c in candidates:
        if c.is_file():
            return c
    return None


class GraphModel:
    """Indexes the node-link JSON once; every kind reads from here."""

    def __init__(self, data: dict, *, extracted_only: bool = False,
                 all_types: bool = False):
        self.data = data
        links = data.get("links")
        if links is None:
            links = data.get("edges", [])  # the --no-cluster writer's key
        self.nodes: dict[str, dict] = {}
        self.src: dict[str, str] = {}        # node id -> normalised source_file
        self.is_file: dict[str, bool] = {}   # node id -> is a file-level node
        self.is_code: dict[str, bool] = {}
        for n in data.get("nodes", []):
            nid = n.get("id")
            if nid is None:
                continue
            nid = str(nid)
            sf = _norm(n.get("source_file") or "")
            self.nodes[nid] = n
            self.src[nid] = sf
            label = _norm(str(n.get("label") or ""))
            # A file node's label is its filename or a path suffix
            # ("app/build.gradle.kts" inside "android/app/...").
            self.is_file[nid] = bool(sf) and (
                sf == label or sf.endswith("/" + label) or Path(sf).name == label
            )
            self.is_code[nid] = (n.get("file_type") or "code") == "code"

        self.all_types = all_types
        self.dep_edges: list[dict] = []   # dependency edges between known nodes
        self.hier_edges: list[dict] = []
        self.out_adj: dict[str, list[int]] = defaultdict(list)  # id -> dep edge idx
        self.in_adj: dict[str, list[int]] = defaultdict(list)
        for e in links:
            s, t = str(e.get("source")), str(e.get("target"))
            if s not in self.nodes or t not in self.nodes:
                continue
            rel = e.get("relation") or "related"
            if rel in HIERARCHY_RELATIONS:
                self.hier_edges.append(e)
                continue
            if extracted_only and (e.get("confidence") or "EXTRACTED") != "EXTRACTED":
                continue
            idx = len(self.dep_edges)
            self.dep_edges.append(e)
            self.out_adj[s].append(idx)
            self.in_adj[t].append(idx)

    # -- selection ---------------------------------------------------------

    def kept(self, nid: str) -> bool:
        """Nodes the structural views (map/area/file/flaws) operate on."""
        return self.all_types or self.is_code.get(nid, False)

    def code_files(self) -> set[str]:
        return {sf for nid, sf in self.src.items() if sf and self.kept(nid)}

    # -- areas -------------------------------------------------------------

    @staticmethod
    def area_of(sf: str, depth: int) -> str:
        parts = _norm(sf).split("/")
        dirs = parts[:-1]
        if not dirs:
            return ROOT_AREA
        return "/".join(dirs[:depth])

    def pick_depth(self, requested: str | int | None) -> int:
        """The smallest folder depth yielding 5-15 areas; else the closest."""
        if requested not in (None, "auto"):
            return max(1, int(requested))
        files = self.code_files()
        lo, hi = AREA_BAND
        best, best_dist = 1, None
        for d in range(1, MAX_AUTO_DEPTH + 1):
            n = len({self.area_of(f, d) for f in files})
            if lo <= n <= hi:
                return d
            dist = (lo - n) if n < lo else (n - hi)
            if best_dist is None or dist < best_dist:
                best, best_dist = d, dist
            if n > hi:
                break  # deeper only adds areas
        return best

    def node_area(self, nid: str, depth: int) -> str:
        sf = self.src.get(nid, "")
        return self.area_of(sf, depth) if sf else EXTERNAL_AREA

    # -- degrees -----------------------------------------------------------

    def dep_degrees(self) -> tuple[Counter, Counter]:
        """(fan_in, fan_out) over dependency edges, kept nodes only."""
        fan_in: Counter = Counter()
        fan_out: Counter = Counter()
        for e in self.dep_edges:
            s, t = str(e["source"]), str(e["target"])
            if s == t or not (self.kept(s) and self.kept(t)):
                continue
            fan_out[s] += 1
            fan_in[t] += 1
        return fan_in, fan_out

    def brief(self, nid: str) -> dict:
        n = self.nodes.get(nid, {})
        return {"id": nid, "label": n.get("label", nid),
                "file": self.src.get(nid, "") or None}

    # -- name resolution ---------------------------------------------------

    def resolve(self, name: str) -> tuple[str | None, list[dict]]:
        """exact id -> exact label -> case-insensitive label -> unique substring.

        Returns (node_id, []) on success, (None, candidates) when ambiguous
        or unknown. Matches run over ALL nodes, code or not: if the user can
        name it, they may ask about it.
        """
        if name in self.nodes:
            return name, []
        by_label = [nid for nid, n in self.nodes.items()
                    if str(n.get("label")) == name]
        if len(by_label) == 1:
            return by_label[0], []
        if by_label:
            return None, [self.brief(nid) for nid in by_label]
        low = name.lower()
        ci = [nid for nid, n in self.nodes.items()
              if str(n.get("label", "")).lower() == low]
        if len(ci) == 1:
            return ci[0], []
        if ci:
            return None, [self.brief(nid) for nid in ci]
        # Substring, tolerant of the extractors' decoration (".onCreate()").
        sub = [nid for nid, n in self.nodes.items()
               if low in str(n.get("label", "")).lower() or low in nid.lower()]
        if len(sub) == 1:
            return sub[0], []
        return None, [self.brief(nid) for nid in sub]


# ---------------------------------------------------------------------------
# Kinds
# ---------------------------------------------------------------------------

def _aggregate(model: GraphModel, group_of) -> tuple[dict, dict]:
    """Aggregate dependency edges between groups.

    group_of(nid) -> group key or None (drop). Self-group edges are dropped —
    the caller wants the picture BETWEEN its boxes.
    Returns ({(a, b): Counter(relation)}, {(a, b): total}).
    """
    rels: dict[tuple, Counter] = defaultdict(Counter)
    for e in model.dep_edges:
        s, t = str(e["source"]), str(e["target"])
        a, b = group_of(s), group_of(t)
        if a is None or b is None or a == b:
            continue
        rels[(a, b)][e.get("relation") or "related"] += 1
    totals = {k: sum(c.values()) for k, c in rels.items()}
    return rels, totals


def _edge_rows(rels: dict, totals: dict, min_edges: int) -> list[dict]:
    rows = []
    for (a, b), total in totals.items():
        if total < min_edges:
            continue
        row = {"from": a, "to": b, "total": total}
        row.update(dict(rels[(a, b)].most_common()))
        rows.append(row)
    rows.sort(key=lambda r: (-r["total"], r["from"], r["to"]))
    return rows


def view_map(model: GraphModel, depth_arg, min_edges: int) -> dict:
    depth = model.pick_depth(depth_arg)
    files_by_area: dict[str, set] = defaultdict(set)
    symbols_by_area: Counter = Counter()
    nodes_by_area: dict[str, list] = defaultdict(list)
    for nid, sf in model.src.items():
        if not sf or not model.kept(nid):
            continue
        area = model.area_of(sf, depth)
        files_by_area[area].add(sf)
        nodes_by_area[area].append(nid)
        if not model.is_file[nid]:
            symbols_by_area[area] += 1

    fan_in, fan_out = model.dep_degrees()
    degree = fan_in + fan_out

    def area_of_node(nid):
        sf = model.src.get(nid, "")
        if not sf or not model.kept(nid):
            return None
        return model.area_of(sf, depth)

    rels, totals = _aggregate(model, area_of_node)

    areas = []
    for area in sorted(files_by_area):
        hubs = sorted(nodes_by_area[area], key=lambda n: -degree[n])[:3]
        mix = Counter(model.nodes[n].get("community_name")
                      for n in nodes_by_area[area]
                      if model.nodes[n].get("community_name"))
        areas.append({
            "id": area, "path": area,
            "files": len(files_by_area[area]),
            "symbols": symbols_by_area[area],
            "hubs": [dict(model.brief(n), degree=degree[n])
                     for n in hubs if degree[n] > 0],
            "community_mix": dict(mix.most_common(3)),
        })
    return {"kind": "map", "depth": depth, "areas": areas,
            "edges": _edge_rows(rels, totals, min_edges)}


def view_area(model: GraphModel, folder: str, min_edges: int) -> dict:
    folder = _norm(folder)
    inside = {nid for nid, sf in model.src.items()
              if model.kept(nid) and sf
              and (sf.startswith(folder + "/") or model.area_of(sf, 99) == folder
                   or (folder == ROOT_AREA and "/" not in sf))}
    if not inside:
        return {"error": f"no files under '{folder}' in the graph",
                "kind": "area", "path": folder}
    files = sorted({model.src[nid] for nid in inside})
    depth = model.pick_depth(None)

    def file_or_area(nid):
        if not model.kept(nid):
            return None
        if nid in inside:
            return ("file", model.src[nid])
        sf = model.src.get(nid, "")
        return ("area", model.area_of(sf, depth)) if sf else ("area", EXTERNAL_AREA)

    rels, totals = _aggregate(model, file_or_area)
    inner_rels = {(a[1], b[1]): c for (a, b), c in rels.items()
                  if a[0] == "file" and b[0] == "file"}
    inner_totals = {k: sum(c.values()) for k, c in inner_rels.items()}
    ports: dict[str, dict] = defaultdict(lambda: {"out": 0, "in": 0})
    for (a, b), total in totals.items():
        if a[0] == "file" and b[0] == "area":
            ports[b[1]]["out"] += total
        elif a[0] == "area" and b[0] == "file":
            ports[a[1]]["in"] += total

    sym_count = Counter(model.src[nid] for nid in inside if not model.is_file[nid])
    return {
        "kind": "area", "path": folder,
        "files": [{"path": f, "symbols": sym_count[f]} for f in files],
        "edges": _edge_rows(inner_rels, inner_totals, min_edges),
        "ports": [{"area": a, **io} for a, io in
                  sorted(ports.items(), key=lambda kv: -(kv[1]["out"] + kv[1]["in"]))],
    }


def view_file(model: GraphModel, path: str) -> dict:
    want = _norm(path)
    matches = sorted({sf for sf in model.src.values()
                      if sf and (sf == want or sf.endswith("/" + want))})
    if not matches:
        return {"error": f"no file matching '{path}' in the graph", "kind": "file"}
    if len(matches) > 1:
        return {"error": "ambiguous file", "kind": "file", "candidates": matches}
    sf = matches[0]
    here = {nid for nid, s in model.src.items() if s == sf}
    symbols = [dict(model.brief(nid),
                    location=model.nodes[nid].get("source_location"))
               for nid in sorted(here) if not model.is_file[nid]]
    depth = model.pick_depth(None)
    intra, external_out, external_in = [], Counter(), Counter()
    for e in model.dep_edges:
        s, t = str(e["source"]), str(e["target"])
        rel = e.get("relation") or "related"
        if s in here and t in here:
            if s != t:
                intra.append({"from": model.nodes[s].get("label", s),
                              "to": model.nodes[t].get("label", t),
                              "relation": rel})
        elif s in here:
            external_out[model.node_area(t, depth)] += 1
        elif t in here:
            external_in[model.node_area(s, depth)] += 1
    return {"kind": "file", "path": sf, "symbols": symbols, "edges": intra,
            "external": {"out": dict(external_out.most_common()),
                         "in": dict(external_in.most_common())}}


def view_node(model: GraphModel, nid: str, hops: int) -> dict:
    depth = model.pick_depth(None)

    def ring(ids: set[str]) -> tuple[dict, dict, set]:
        out_r: dict[str, list] = defaultdict(list)
        in_r: dict[str, list] = defaultdict(list)
        seen = set()
        for i in ids:
            for idx in model.out_adj.get(i, ()):
                e = model.dep_edges[idx]
                t = str(e["target"])
                out_r[e.get("relation") or "related"].append(model.brief(t))
                seen.add(t)
            for idx in model.in_adj.get(i, ()):
                e = model.dep_edges[idx]
                s = str(e["source"])
                in_r[e.get("relation") or "related"].append(model.brief(s))
                seen.add(s)
        return dict(out_r), dict(in_r), seen

    out1, in1, seen = ring({nid})
    result = {"kind": "node",
              "center": dict(model.brief(nid), area=model.node_area(nid, depth)),
              "hops": hops, "out": out1, "in": in1}
    if hops >= 2:
        out2, in2, _ = ring(seen - {nid})
        result["second_ring"] = {"out": out2, "in": in2}
    return result


def view_impact(model: GraphModel, nid: str, depth_limit: int) -> dict:
    """Reverse traversal: who (transitively) depends on this node.

    An edge u -> v (u calls/imports/references v) means u depends on v, so
    impact walks INBOUND edges outward from the centre.
    """
    area_depth = model.pick_depth(None)
    visited = {nid}
    frontier = {nid}
    rings = []
    for d in range(1, depth_limit + 1):
        nxt = set()
        for i in frontier:
            for idx in model.in_adj.get(i, ()):
                s = str(model.dep_edges[idx]["source"])
                if s not in visited:
                    visited.add(s)
                    nxt.add(s)
        if not nxt:
            break
        rings.append({"depth": d,
                      "nodes": [dict(model.brief(n),
                                     area=model.node_area(n, area_depth))
                                for n in sorted(nxt)]})
        frontier = nxt
    by_area: Counter = Counter()
    for r in rings:
        for n in r["nodes"]:
            by_area[n["area"]] += 1
    return {"kind": "impact",
            "center": dict(model.brief(nid), area=model.node_area(nid, area_depth)),
            "depth": depth_limit, "rings": rings,
            "areas": dict(by_area.most_common()),
            "total": sum(by_area.values())}


def _bfs_path(model: GraphModel, a: str, b: str, *, undirected: bool):
    """Shortest dependency path as [(edge, node), ...]; None if unreachable."""
    prev: dict[str, tuple[str, dict]] = {}
    frontier = [a]
    seen = {a}
    while frontier:
        nxt = []
        for u in frontier:
            hops = [(model.dep_edges[i], str(model.dep_edges[i]["target"]))
                    for i in model.out_adj.get(u, ())]
            if undirected:
                hops += [(model.dep_edges[i], str(model.dep_edges[i]["source"]))
                         for i in model.in_adj.get(u, ())]
            for e, v in hops:
                if v in seen:
                    continue
                seen.add(v)
                prev[v] = (u, e)
                if v == b:
                    path = []
                    while v != a:
                        u2, e2 = prev[v]
                        path.append((e2, v))
                        v = u2
                    return list(reversed(path))
                nxt.append(v)
        frontier = nxt
    return None


def view_trace(model: GraphModel, a: str, b: str) -> dict:
    steps = _bfs_path(model, a, b, undirected=False)
    direction = "directed"
    if steps is None:
        steps = _bfs_path(model, a, b, undirected=True)
        direction = "undirected"
    if steps is None:
        return {"kind": "trace", "error": "no path found",
                "from": model.brief(a), "to": model.brief(b)}
    path = [model.brief(a)] + [model.brief(v) for _, v in steps]
    edges = [{"from": str(e["source"]), "to": str(e["target"]),
              "from_label": model.nodes[str(e["source"])].get("label"),
              "to_label": model.nodes[str(e["target"])].get("label"),
              "relation": e.get("relation") or "related"} for e, _ in steps]
    return {"kind": "trace", "direction": direction, "path": path, "edges": edges}


def view_reach(model: GraphModel, nid: str, depth_limit: int) -> dict:
    visited = {nid}
    frontier = {nid}
    levels = []
    for d in range(1, depth_limit + 1):
        nxt = set()
        for i in frontier:
            for idx in model.out_adj.get(i, ()):
                t = str(model.dep_edges[idx]["target"])
                if t not in visited:
                    visited.add(t)
                    nxt.add(t)
        if not nxt:
            break
        levels.append({"depth": d,
                       "nodes": [model.brief(n) for n in sorted(nxt)]})
        frontier = nxt
    return {"kind": "trace", "mode": "reachable", "from": model.brief(nid),
            "depth": depth_limit, "levels": levels,
            "total": sum(len(l["nodes"]) for l in levels)}


_ENTRY_LABELS = {"main", "__main__", "_main", "main()", ".main()", "app", "index"}


def _looks_like_entry(model: GraphModel, nid: str) -> bool:
    label = str(model.nodes[nid].get("label", "")).strip().lower()
    if label.strip(".()") in {e.strip(".()") for e in _ENTRY_LABELS}:
        return True
    sf = model.src.get(nid, "").lower()
    parts = sf.split("/")
    name = Path(sf).stem
    return (name in ("main", "__main__", "index", "app")
            or any(p in ("tests", "test") or p.startswith("test_") for p in parts)
            or name.startswith("test_") or name.endswith("_test")
            or name.endswith(".test") or name.endswith(".spec"))


def _scc_cycles(edges: dict[tuple, int]) -> list[dict]:
    """Strongly connected components with >1 member, smallest first.

    Tries networkx (a core dependency of the package); falls back to an
    iterative Tarjan so the module also works standalone.
    """
    members_adj: dict = defaultdict(set)
    for (a, b) in edges:
        members_adj[a].add(b)
        members_adj.setdefault(b, set())
    try:
        import networkx as nx
        g = nx.DiGraph()
        for (a, b), w in edges.items():
            g.add_edge(a, b, weight=w)
        sccs = [sorted(c) for c in nx.strongly_connected_components(g) if len(c) > 1]
    except ImportError:  # pragma: no cover - networkx ships with the package
        sccs = _tarjan(members_adj)
    out = []
    for comp in sorted(sccs, key=len):
        cset = set(comp)
        closing = [{"from": a, "to": b, "count": w}
                   for (a, b), w in sorted(edges.items(), key=lambda kv: -kv[1])
                   if a in cset and b in cset]
        out.append({"members": comp, "closing_edges": closing})
    return out


def _tarjan(adj: dict) -> list[list]:
    index: dict = {}
    low: dict = {}
    on_stack: set = set()
    stack: list = []
    result = []
    counter = [0]
    for root in list(adj):
        if root in index:
            continue
        work = [(root, iter(sorted(adj.get(root, ()))))]
        index[root] = low[root] = counter[0]
        counter[0] += 1
        stack.append(root)
        on_stack.add(root)
        while work:
            v, it = work[-1]
            advanced = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = counter[0]
                    counter[0] += 1
                    stack.append(w)
                    on_stack.add(w)
                    work.append((w, iter(sorted(adj.get(w, ())))))
                    advanced = True
                    break
                if w in on_stack:
                    low[v] = min(low[v], index[w])
            if advanced:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index[v]:
                comp = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                if len(comp) > 1:
                    result.append(sorted(comp))
    return result


def _p95(values: list[int]) -> int:
    if not values:
        return 0
    ordered = sorted(values)
    return ordered[int(0.95 * (len(ordered) - 1))]


def view_flaws(model: GraphModel, checks: list[str]) -> dict:
    result: dict = {"kind": "flaws", "checks": checks}
    depth = model.pick_depth(None)

    if "cycles" in checks:
        def by_area(nid):
            sf = model.src.get(nid, "")
            return model.area_of(sf, depth) if sf and model.kept(nid) else None

        def by_file(nid):
            sf = model.src.get(nid, "")
            return sf if sf and model.kept(nid) else None

        cycles = []
        for level, group_of in (("area", by_area), ("file", by_file)):
            _, totals = _aggregate(model, group_of)
            for c in _scc_cycles(totals):
                cycles.append(dict(c, level=level))
        result["cycles"] = cycles

    if "hubs" in checks:
        fan_in, fan_out = model.dep_degrees()
        nids = {n for n in list(fan_in) + list(fan_out)}
        thr_in = max(20, _p95([fan_in[n] for n in nids]))
        thr_out = max(20, _p95([fan_out[n] for n in nids]))
        hubs = [dict(model.brief(n), fan_in=fan_in[n], fan_out=fan_out[n])
                for n in nids if fan_in[n] > thr_in or fan_out[n] > thr_out]
        hubs.sort(key=lambda h: -(h["fan_in"] + h["fan_out"]))
        result["hubs"] = hubs
        result["hub_thresholds"] = {"fan_in": thr_in, "fan_out": thr_out}

    if "orphans" in checks:
        fan_in, _ = model.dep_degrees()
        # Orphan FILES: no dependency edge from outside reaches the file or
        # anything in it. Reported at file level because a per-symbol list
        # buries the signal (helpers reached via dynamic dispatch are legion).
        inbound_files: set[str] = set()
        for e in model.dep_edges:
            s, t = str(e["source"]), str(e["target"])
            if not (model.kept(s) and model.kept(t)):
                continue
            fs, ft = model.src.get(s, ""), model.src.get(t, "")
            if ft and fs != ft:
                inbound_files.add(ft)
        orphans = []
        for sf in sorted(model.code_files()):
            if sf in inbound_files:
                continue
            ids = [nid for nid, s in model.src.items() if s == sf]
            if any(_looks_like_entry(model, nid) for nid in ids):
                continue
            orphans.append({"file": sf,
                            "symbols": sum(1 for nid in ids
                                           if not model.is_file[nid])})
        result["orphans"] = orphans

    result["summary"] = {
        "cycles": len(result.get("cycles", [])),
        "hubs": len(result.get("hubs", [])),
        "orphans": len(result.get("orphans", [])),
    }
    return result


def view_stats(model: GraphModel, graph_path: Path, project: str) -> dict:
    data = model.data
    rels = Counter((e.get("relation") or "related")
                   for e in model.dep_edges + model.hier_edges)
    types = Counter((n.get("file_type") or "code") for n in model.nodes.values())
    depth = model.pick_depth(None)
    areas = {model.area_of(f, depth) for f in model.code_files()}
    built = data.get("built_at_commit")
    head = None
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"],
                              cwd=Path(project).resolve(), check=False,
                              capture_output=True, text=True, timeout=10)
        head = proc.stdout.strip() or None if proc.returncode == 0 else None
    except OSError:
        head = None
    return {"kind": "stats", "graph": str(graph_path),
            "nodes": len(model.nodes),
            "edges": len(model.dep_edges) + len(model.hier_edges),
            "dependency_edges": len(model.dep_edges),
            "relations": dict(rels.most_common()),
            "file_types": dict(types.most_common()),
            "files": len({s for s in model.src.values() if s}),
            "areas": {"depth": depth, "count": len(areas)},
            "built_at_commit": built, "git_head": head,
            "stale": (bool(built and head and built != head) or None)}


# ---------------------------------------------------------------------------
# Text rendering (the --json path is the primary consumer; this is for humans)
# ---------------------------------------------------------------------------

def _print_text(result: dict) -> None:
    kind = result.get("kind")
    if "error" in result:
        print(f"error: {result['error']}")
        for c in result.get("candidates", [])[:20]:
            print(f"  - {c if isinstance(c, str) else c.get('label')}")
        return
    if kind == "map":
        print(f"Areas (folder depth {result['depth']}):")
        for a in result["areas"]:
            hubs = ", ".join(h["label"] for h in a["hubs"]) or "-"
            print(f"  {a['path']:<30} {a['files']:>4} files "
                  f"{a['symbols']:>5} symbols   hubs: {hubs}")
        print("Edges between areas:")
        for e in result["edges"][:30]:
            rels = ", ".join(f"{k} {v}" for k, v in e.items()
                             if k not in ("from", "to", "total"))
            print(f"  {e['from']} -> {e['to']}  ({e['total']}: {rels})")
    elif kind == "area":
        print(f"{result['path']}: {len(result['files'])} files")
        for f in result["files"]:
            print(f"  {f['path']} ({f['symbols']} symbols)")
        for e in result["edges"][:30]:
            print(f"  {e['from']} -> {e['to']} ({e['total']})")
        for p in result["ports"]:
            print(f"  port {p['area']}: out {p['out']}, in {p['in']}")
    elif kind == "file":
        print(f"{result['path']}: {len(result['symbols'])} symbols")
        for s in result["symbols"]:
            print(f"  {s['label']} {s.get('location') or ''}")
        for e in result["edges"]:
            print(f"  {e['from']} --{e['relation']}--> {e['to']}")
        ext = result["external"]
        if ext["out"]:
            print("  uses:", ", ".join(f"{a} ({n})" for a, n in ext["out"].items()))
        if ext["in"]:
            print("  used by:", ", ".join(f"{a} ({n})" for a, n in ext["in"].items()))
    elif kind == "node":
        c = result["center"]
        print(f"{c['label']}  ({c.get('file') or 'external'})")
        for rel, targets in result["out"].items():
            print(f"  {rel} -> " + ", ".join(t["label"] for t in targets[:15]))
        for rel, sources in result["in"].items():
            print(f"  <- {rel} " + ", ".join(s["label"] for s in sources[:15]))
    elif kind == "impact":
        c = result["center"]
        print(f"Impact of {c['label']}: {result['total']} dependents "
              f"within {result['depth']} hops")
        for r in result["rings"]:
            labels = ", ".join(n["label"] for n in r["nodes"][:15])
            more = "" if len(r["nodes"]) <= 15 else f" (+{len(r['nodes']) - 15} more)"
            print(f"  ring {r['depth']}: {labels}{more}")
        for area, n in result["areas"].items():
            print(f"  {area}: {n}")
    elif kind == "trace" and result.get("mode") == "reachable":
        print(f"Reachable from {result['from']['label']}: {result['total']} nodes")
        for l in result["levels"]:
            labels = ", ".join(n["label"] for n in l["nodes"][:15])
            print(f"  depth {l['depth']}: {labels}")
    elif kind == "trace":
        arrow = " -> " if result["direction"] == "directed" else " -- "
        print(arrow.join(n["label"] for n in result["path"]))
        for e in result["edges"]:
            print(f"  {e.get('from_label') or e['from']} "
                  f"--{e['relation']}--> {e.get('to_label') or e['to']}")
        if result["direction"] == "undirected":
            print("  (no directed path; this is an undirected connection)")
    elif kind == "flaws":
        s = result["summary"]
        print(f"cycles: {s['cycles']}  hub overload: {s['hubs']}  "
              f"orphan files: {s['orphans']}  (signals to look at, not verdicts)")
        for c in result.get("cycles", [])[:10]:
            print(f"  cycle ({c['level']}): " + " <-> ".join(c["members"]))
        for h in result.get("hubs", [])[:10]:
            print(f"  hub: {h['label']} (in {h['fan_in']}, out {h['fan_out']}) "
                  f"{h.get('file') or ''}")
        for o in result.get("orphans", [])[:10]:
            print(f"  orphan file: {o['file']} ({o['symbols']} symbols)")
        if len(result.get("orphans", [])) > 10:
            print(f"  ... and {len(result['orphans']) - 10} more orphan files")
    elif kind == "stats":
        for k in ("graph", "nodes", "edges", "dependency_edges", "files"):
            print(f"{k}: {result[k]}")
        print(f"areas: {result['areas']['count']} at depth {result['areas']['depth']}")
        print(f"relations: " + ", ".join(f"{k} {v}"
                                         for k, v in result["relations"].items()))
        if result.get("stale"):
            print(f"stale: graph built at {result['built_at_commit'][:12]}, "
                  f"HEAD is {result['git_head'][:12]} - run: halal-graphify update .")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="halal-graphify view",
        description="Architecture views over graphify-out/graph.json (no LLM).")
    sub = ap.add_subparsers(dest="view_kind", required=True)

    def common(p):
        p.add_argument("--project", default=".",
                       help="project root to locate graphify-out under (default: cwd)")
        p.add_argument("--graph", default=None, help="explicit path to graph.json")
        p.add_argument("--json", action="store_true", dest="as_json",
                       help="machine-readable output")
        p.add_argument("--extracted-only", action="store_true",
                       help="drop INFERRED/AMBIGUOUS edges")
        p.add_argument("--all-types", action="store_true",
                       help="include document/concept nodes in structural views")

    p = sub.add_parser("map", help="areas and the edges between them")
    p.add_argument("--depth", default="auto", help="folder depth or 'auto' (5-15 areas)")
    p.add_argument("--min-edges", type=int, default=1)
    common(p)

    p = sub.add_parser("area", help="files inside one folder")
    p.add_argument("folder")
    p.add_argument("--min-edges", type=int, default=1)
    common(p)

    p = sub.add_parser("file", help="symbols in one file")
    p.add_argument("path")
    common(p)

    p = sub.add_parser("node", help="one symbol's neighbourhood")
    p.add_argument("name")
    p.add_argument("--hops", type=int, choices=(1, 2), default=1)
    common(p)

    p = sub.add_parser("impact", help="who transitively depends on a symbol")
    p.add_argument("name")
    p.add_argument("--depth", type=int, default=3)
    common(p)

    p = sub.add_parser("trace", help="shortest dependency path A -> B, "
                                     "or --from X for reachability")
    p.add_argument("a", nargs="?")
    p.add_argument("b", nargs="?")
    p.add_argument("--from", dest="from_", metavar="X",
                   help="forward reachability instead of a path")
    p.add_argument("--depth", type=int, default=3,
                   help="reachability depth (with --from)")
    common(p)

    p = sub.add_parser("flaws", help="cycles, hub overload, orphans")
    p.add_argument("--checks", default="cycles,hubs,orphans")
    common(p)

    p = sub.add_parser("stats", help="counts, area depth, staleness")
    common(p)
    return ap


def _emit(result: dict, as_json: bool) -> int:
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        _print_text(result)
    return 1 if "error" in result and "candidates" not in result else \
        (2 if "candidates" in result else 0)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    graph_path = find_graph(args.project, args.graph)
    if graph_path is None:
        msg = ("no graph found: no graphify-out/graph.json at or above "
               f"'{Path(args.project).resolve()}'.\n"
               "Build one for free (AST only, no LLM):\n"
               f'  halal-graphify extract "{args.project}" --code-only')
        if args.as_json:
            print(json.dumps({"error": msg}))
        else:
            print(msg, file=sys.stderr)
        return 3

    try:
        data = json.loads(graph_path.read_text(encoding="utf-8"))
        model = GraphModel(data, extracted_only=args.extracted_only,
                           all_types=args.all_types)
    except (OSError, ValueError) as exc:
        print(f"error: could not load {graph_path}: {exc}", file=sys.stderr)
        return 1

    kind = args.view_kind
    needs_name = kind in ("node", "impact") or (
        kind == "trace" and not getattr(args, "from_", None))

    if kind == "map":
        result = view_map(model, args.depth, args.min_edges)
    elif kind == "area":
        result = view_area(model, args.folder, args.min_edges)
    elif kind == "file":
        result = view_file(model, args.path)
    elif kind == "stats":
        result = view_stats(model, graph_path, args.project)
    elif kind == "flaws":
        checks = [c.strip() for c in args.checks.split(",") if c.strip()]
        unknown = set(checks) - {"cycles", "hubs", "orphans"}
        if unknown:
            print(f"error: unknown checks: {', '.join(sorted(unknown))} "
                  "(valid: cycles, hubs, orphans)", file=sys.stderr)
            return 1
        result = view_flaws(model, checks)
    elif needs_name:
        names = [args.name] if kind in ("node", "impact") else [args.a, args.b]
        if kind == "trace" and (not args.a or not args.b):
            print("error: trace needs two names, or --from X", file=sys.stderr)
            return 1
        resolved = []
        for name in names:
            nid, candidates = model.resolve(name)
            if nid is None:
                result = {"kind": kind, "error": f"'{name}' is ambiguous"
                          if candidates else f"'{name}' not found in the graph",
                          "candidates": candidates[:20]} if candidates else \
                         {"kind": kind, "error": f"'{name}' not found in the graph"}
                return _emit(result, args.as_json)
            resolved.append(nid)
        if kind == "node":
            result = view_node(model, resolved[0], args.hops)
        elif kind == "impact":
            result = view_impact(model, resolved[0], args.depth)
        else:
            result = view_trace(model, resolved[0], resolved[1])
    else:  # trace --from
        nid, candidates = model.resolve(args.from_)
        if nid is None:
            result = {"kind": "trace",
                      "error": f"'{args.from_}' is ambiguous" if candidates
                      else f"'{args.from_}' not found in the graph"}
            if candidates:
                result["candidates"] = candidates[:20]
            return _emit(result, args.as_json)
        result = view_reach(model, nid, args.depth)

    return _emit(result, args.as_json)


if __name__ == "__main__":
    raise SystemExit(main())
