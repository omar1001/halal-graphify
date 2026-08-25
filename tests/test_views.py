"""Tests for the fork-only `view` verb (halal_graphify/views.py).

The fixture graph is synthetic and small, with every reportable structure
planted deliberately: six top-level areas (so `--depth auto` lands inside the
5-15 band), a two-file dependency cycle that is also an area cycle, one node
with fan-in above the hub threshold, one orphan file, entry-point and test
files that must NOT count as orphans, document nodes that the structural
views must exclude by default, and one node whose source_file uses Windows
backslashes (the plan's named risk).
"""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from halal_graphify.views import (
    GraphModel, find_graph, main, view_area, view_file, view_flaws,
    view_impact, view_map, view_node, view_reach, view_stats, view_trace,
)


def _node(nid, label, source_file, file_type="code"):
    return {"id": nid, "label": label, "source_file": source_file,
            "file_type": file_type, "community_name": "test-community"}


def _edge(source, target, relation, confidence="EXTRACTED"):
    return {"source": source, "target": target, "relation": relation,
            "confidence": confidence, "weight": 1.0}


def make_graph() -> dict:
    nodes = [
        # six top-level areas: core, api, db, ui, util, tools
        _node("core_engine_py", "engine.py", "core/engine.py"),
        _node("core_engine", "Engine", "core/engine.py"),
        _node("core_engine_run", ".run()", "core/engine.py"),
        _node("api_server_py", "server.py", "api/server.py"),
        _node("api_server", "Server", "api/server.py"),
        _node("db_store_py", "store.py", "db/store.py"),
        _node("db_store", "Store", "db/store.py"),
        _node("ui_app_py", "app.py", "ui/app.py"),
        _node("ui_app", "App", "ui/app.py"),
        _node("util_helpers_py", "helpers.py", "util/helpers.py"),
        _node("util_helpers", "helpers", "util/helpers.py"),
        # Windows-style path (risk table: normalise to forward slashes)
        _node("tools_gen", "Generator", "tools\\gen.py"),
        _node("tools_gen_py", "gen.py", "tools\\gen.py"),
        # cycle: a/x.py <-> b/y.py (adds two more areas: a, b -> 8 total)
        _node("a_x_py", "x.py", "a/x.py"),
        _node("a_x", "XThing", "a/x.py"),
        _node("b_y_py", "y.py", "b/y.py"),
        _node("b_y", "YThing", "b/y.py"),
        # orphan file: nothing depends on it, and it is not an entry point
        _node("util_dead_py", "dead.py", "util/dead.py"),
        _node("util_dead", "DeadCode", "util/dead.py"),
        # entry point + test file: zero inbound but NOT orphans
        _node("main_py", "main.py", "main.py"),
        _node("main_fn", "main", "main.py"),
        _node("test_engine_py", "test_engine.py", "tests/test_engine.py"),
        # a document node: excluded from structural views by default
        _node("readme_sec", "Introduction", "README.md", file_type="document"),
        # an external symbol (no source_file)
        _node("external_lib", "ExternalLib", ""),
    ]
    edges = [
        # hierarchy
        _edge("core_engine_py", "core_engine", "contains"),
        _edge("core_engine", "core_engine_run", "method"),
        _edge("api_server_py", "api_server", "contains"),
        _edge("db_store_py", "db_store", "contains"),
        _edge("ui_app_py", "ui_app", "contains"),
        _edge("a_x_py", "a_x", "contains"),
        _edge("b_y_py", "b_y", "contains"),
        _edge("util_dead_py", "util_dead", "contains"),
        # dependencies: ui -> api -> core -> db; everything -> util
        _edge("ui_app", "api_server", "calls"),
        _edge("api_server", "core_engine", "calls"),
        _edge("api_server", "core_engine_run", "calls"),
        _edge("core_engine_run", "db_store", "calls"),
        _edge("ui_app", "util_helpers", "imports"),
        _edge("api_server", "util_helpers", "imports"),
        _edge("core_engine", "util_helpers", "imports"),
        _edge("main_fn", "ui_app", "calls"),
        _edge("test_engine_py", "core_engine", "references"),
        _edge("core_engine", "external_lib", "inherits"),
        _edge("tools_gen", "core_engine", "references", confidence="INFERRED"),
        # the planted cycle
        _edge("a_x", "b_y", "calls"),
        _edge("b_y", "a_x", "calls"),
        # doc -> code reference (must not leak into the default map)
        _edge("readme_sec", "core_engine", "references"),
    ]
    # hub overload: 25 callers of util_helpers pushes fan-in past max(20, p95)
    for i in range(25):
        nodes.append(_node(f"api_h{i}", f".handler{i}()", "api/server.py"))
        edges.append(_edge("api_server_py", f"api_h{i}", "contains"))
        edges.append(_edge(f"api_h{i}", "util_helpers", "calls"))
    return {"directed": True, "multigraph": True, "graph": {},
            "nodes": nodes, "links": edges, "built_at_commit": "abc123"}


def model(**kw) -> GraphModel:
    return GraphModel(make_graph(), **kw)


class TestModel(unittest.TestCase):
    def test_windows_paths_are_normalised(self):
        m = model()
        self.assertEqual(m.src["tools_gen"], "tools/gen.py")
        self.assertIn("tools/gen.py", m.code_files())

    def test_file_node_detection(self):
        m = model()
        self.assertTrue(m.is_file["core_engine_py"])
        self.assertFalse(m.is_file["core_engine"])
        self.assertFalse(m.is_file["external_lib"])

    def test_hierarchy_vs_dependency_split(self):
        m = model()
        rels = {e["relation"] for e in m.dep_edges}
        self.assertNotIn("contains", rels)
        self.assertNotIn("method", rels)
        self.assertIn("calls", rels)

    def test_extracted_only_drops_inferred(self):
        keep = model()
        strict = model(extracted_only=True)
        self.assertEqual(len(keep.dep_edges) - len(strict.dep_edges), 1)

    def test_auto_depth_lands_in_band(self):
        m = model()
        d = m.pick_depth(None)
        areas = {m.area_of(f, d) for f in m.code_files()}
        self.assertTrue(5 <= len(areas) <= 15, areas)


class TestResolve(unittest.TestCase):
    def test_exact_id_and_label(self):
        m = model()
        self.assertEqual(m.resolve("core_engine")[0], "core_engine")
        self.assertEqual(m.resolve("Engine")[0], "core_engine")

    def test_case_insensitive_label(self):
        m = model()
        self.assertEqual(m.resolve("engine")[0], "core_engine")

    def test_unique_substring(self):
        m = model()
        self.assertEqual(m.resolve("DeadCo")[0], "util_dead")

    def test_ambiguous_returns_candidates(self):
        m = model()
        nid, candidates = m.resolve("handler")
        self.assertIsNone(nid)
        self.assertGreater(len(candidates), 1)

    def test_unknown_returns_empty(self):
        m = model()
        nid, candidates = m.resolve("NoSuchThing")
        self.assertIsNone(nid)
        self.assertEqual(candidates, [])


class TestMap(unittest.TestCase):
    def test_map_shape_and_doc_exclusion(self):
        result = view_map(model(), "auto", 1)
        paths = {a["path"] for a in result["areas"]}
        self.assertIn("core", paths)
        self.assertIn("(root)", paths)      # main.py groups under (root)
        self.assertNotIn("README.md", paths)  # doc node excluded by default
        ui_api = [e for e in result["edges"]
                  if e["from"] == "ui" and e["to"] == "api"]
        self.assertEqual(ui_api[0]["calls"], 1)

    def test_all_types_includes_documents(self):
        result = view_map(model(all_types=True), "auto", 1)
        self.assertIn("(root)", {a["path"] for a in result["areas"]})
        symbols = {a["path"]: a["symbols"] for a in result["areas"]}
        self.assertGreaterEqual(symbols["(root)"], 2)  # main + readme section

    def test_min_edges_filters(self):
        result = view_map(model(), "auto", 2)
        for e in result["edges"]:
            self.assertGreaterEqual(e["total"], 2)


class TestAreaAndFile(unittest.TestCase):
    def test_area_lists_files_and_ports(self):
        result = view_area(model(), "core", 1)
        self.assertEqual([f["path"] for f in result["files"]], ["core/engine.py"])
        port_areas = {p["area"] for p in result["ports"]}
        self.assertIn("db", port_areas)   # core calls db
        self.assertIn("api", port_areas)  # api calls core

    def test_area_unknown_folder_errors(self):
        result = view_area(model(), "nope", 1)
        self.assertIn("error", result)

    def test_file_symbols_and_external(self):
        result = view_file(model(), "core/engine.py")
        labels = {s["label"] for s in result["symbols"]}
        self.assertEqual(labels, {"Engine", ".run()"})
        self.assertIn("db", result["external"]["out"])
        self.assertIn("api", result["external"]["in"])

    def test_file_suffix_match(self):
        result = view_file(model(), "engine.py")
        self.assertEqual(result["path"], "core/engine.py")


class TestNodeImpactTrace(unittest.TestCase):
    def test_node_neighbourhood(self):
        result = view_node(model(), "core_engine", 1)
        out_rels = result["out"]
        self.assertIn("imports", out_rels)
        in_labels = {n["label"] for rel in result["in"].values() for n in rel}
        self.assertIn("Server", in_labels)

    def test_impact_rings(self):
        result = view_impact(model(), "db_store", 3)
        ring1 = {n["label"] for n in result["rings"][0]["nodes"]}
        self.assertEqual(ring1, {".run()"})
        all_nodes = {n["label"] for r in result["rings"] for n in r["nodes"]}
        self.assertIn("Server", all_nodes)  # Server -> Engine -> .run() -> Store
        self.assertEqual(result["total"],
                         sum(len(r["nodes"]) for r in result["rings"]))

    def test_trace_directed(self):
        result = view_trace(model(), "ui_app", "db_store")
        self.assertEqual(result["direction"], "directed")
        labels = [n["label"] for n in result["path"]]
        self.assertEqual(labels[0], "App")
        self.assertEqual(labels[-1], "Store")

    def test_trace_undirected_fallback(self):
        # Store has no outbound path to App; undirected connection exists.
        result = view_trace(model(), "db_store", "ui_app")
        self.assertEqual(result["direction"], "undirected")

    def test_trace_reachable(self):
        result = view_reach(model(), "ui_app", 3)
        self.assertGreaterEqual(result["total"], 3)
        self.assertEqual(result["levels"][0]["depth"], 1)


class TestFlaws(unittest.TestCase):
    def test_finds_planted_cycle_at_both_levels(self):
        result = view_flaws(model(), ["cycles"])
        levels = {c["level"]: c for c in result["cycles"]}
        self.assertIn("area", levels)
        self.assertIn("file", levels)
        self.assertEqual(set(levels["file"]["members"]), {"a/x.py", "b/y.py"})
        self.assertTrue(levels["file"]["closing_edges"])

    def test_finds_planted_hub(self):
        result = view_flaws(model(), ["hubs"])
        self.assertEqual(len(result["hubs"]), 1)
        self.assertEqual(result["hubs"][0]["label"], "helpers")
        self.assertGreater(result["hubs"][0]["fan_in"], 20)

    def test_orphans_exclude_entry_and_tests(self):
        result = view_flaws(model(), ["orphans"])
        files = {o["file"] for o in result["orphans"]}
        self.assertIn("util/dead.py", files)
        self.assertNotIn("main.py", files)
        self.assertNotIn("tests/test_engine.py", files)

    def test_summary_counts(self):
        result = view_flaws(model(), ["cycles", "hubs", "orphans"])
        self.assertEqual(result["summary"]["hubs"], 1)
        self.assertGreaterEqual(result["summary"]["cycles"], 2)


class TestStatsAndCli(unittest.TestCase):
    def _write_graph(self, root: Path) -> Path:
        out = root / "graphify-out"
        out.mkdir(parents=True)
        gp = out / "graph.json"
        gp.write_text(json.dumps(make_graph()), encoding="utf-8")
        return gp

    def test_find_graph_walks_upward(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            gp = self._write_graph(root)
            sub = root / "core" / "deeper"
            sub.mkdir(parents=True)
            # Path.resolve() expands Windows 8.3 short names; resolve both sides.
            self.assertEqual(find_graph(str(sub), None), gp.resolve())
            self.assertEqual(find_graph(str(root), None), gp.resolve())

    def test_find_graph_missing_returns_none(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(find_graph(tmp, None))

    def test_stats_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            gp = self._write_graph(Path(tmp))
            m = model()
            result = view_stats(m, gp, tmp)
            self.assertEqual(result["nodes"], len(m.nodes))
            self.assertEqual(result["built_at_commit"], "abc123")
            self.assertIn("calls", result["relations"])

    def test_cli_map_json(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            gp = self._write_graph(Path(tmp))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["map", "--graph", str(gp), "--json"])
            self.assertEqual(code, 0)
            data = json.loads(buf.getvalue())
            self.assertEqual(data["kind"], "map")
            self.assertTrue(5 <= len(data["areas"]) <= 15)

    def test_cli_ambiguous_name_exits_2(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            gp = self._write_graph(Path(tmp))
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = main(["impact", "handler", "--graph", str(gp), "--json"])
            self.assertEqual(code, 2)
            data = json.loads(buf.getvalue())
            self.assertTrue(data["candidates"])

    def test_cli_no_graph_exits_3(self):
        import contextlib
        import io
        with tempfile.TemporaryDirectory() as tmp:
            buf = io.StringIO()
            err = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
                code = main(["map", "--project", tmp])
            self.assertEqual(code, 3)
            self.assertIn("extract", err.getvalue())


if __name__ == "__main__":
    unittest.main()
