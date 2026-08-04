# GDScript / Godot extractor. FORK-OWNED -- see the note at the bottom.
#
# Standalone AST + regex extractor for Godot's GDScript (.gd) source and its
# scene/resource text formats (.tscn/.tres). Ported from the graphify-godot
# fork (Bruno Hidalgo, MIT) onto upstream's extractors/ layout, sharing
# _make_id / _read_text with the other extractors via .base rather than
# carrying its own copies (upstream's make_id already relativises paths for
# cross-machine-stable IDs, so the fork's bespoke _ID_ROOT helper is dropped).
#
#   .gd    -> tree-sitter AST: class_name, extends (inherits), inner classes,
#             func (calls), signal (defs/emits/connects), preload/load imports.
#   .tscn  -> regex: ext_resource script bindings, node instances, signal
#   .tres  -> connections resolved against the project.godot root.
#
# Upstream Graphify does not support GDScript at all: every .gd file lands in
# `unclassified`, so a Godot project graphs to nothing useful. This module is
# the fork's own addition and is NOT regenerated from upstream -- it lives in
# overlay/ and is copied in by sync.py after rename.py has run. Edit it HERE,
# never in the generated package copy, or the next sync erases the change.
#
# Only .gd needs a tree-sitter grammar. .tscn/.tres are pure regex and work
# with no extra dependency at all.
#
# Lineage / attribution:
#   Bruno Hidalgo  -- original GDScript backend (hidalgob/graphify-godot, MIT)
#   Epic Millennium -- port onto Graphify v0.9.23
#   this fork      -- carried onto v0.9.32+ as a regeneration-safe overlay
from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from halal_graphify.extractors.base import _file_stem, _make_id, _read_text


_GDSCRIPT_PROJECT_ROOT_CACHE: dict[str, Path | None] = {}


def _gdscript_project_root(path: Path) -> Path | None:
    """Walk up from path looking for project.godot; cache by parent dir."""
    start = path.parent
    key = str(start)
    if key in _GDSCRIPT_PROJECT_ROOT_CACHE:
        return _GDSCRIPT_PROJECT_ROOT_CACHE[key]
    cur = start
    found: Path | None = None
    while True:
        if (cur / "project.godot").exists():
            found = cur
            break
        parent = cur.parent
        if parent == cur:
            break
        cur = parent
    _GDSCRIPT_PROJECT_ROOT_CACHE[key] = found
    return found


def _gdscript_resolve_res_path(raw: str, current: Path) -> Path | None:
    """Resolve a Godot resource path (res://foo/bar.gd or relative) to a filesystem Path."""
    if raw.startswith("res://"):
        proot = _gdscript_project_root(current)
        if proot is None:
            return None
        return proot / raw[6:]
    if raw.startswith("user://") or raw.startswith("uid://"):
        return None
    # Relative path — resolve against the file's directory
    return current.parent / raw


def _resource_target_id(resolved: Path, source: Path) -> str:
    """Node ID for an edge to a resolved resource path, safe against absolute
    filesystem paths leaking into the graph.

    Corpus files (code/docs halal-graphify extracts as nodes) keep the absolute-derived
    id: extract()'s id-remap canonicalises them to the repo-relative form and
    rewrites matching edge endpoints, so they stay correct even when the scan root
    sits above the Godot project (monorepo). Non-corpus resources (.glb/.png/.ogg…)
    are never in the scanned corpus, so the remap never sees them — build a portable
    project-relative id here (mirroring extract._file_node_id) so their endpoints
    don't embed a machine-specific path that would break graph portability and
    churn the graph.json merge driver across machines."""
    from halal_graphify.detect import CODE_EXTENSIONS, DOC_EXTENSIONS

    if resolved.suffix.lower() in CODE_EXTENSIONS or resolved.suffix.lower() in DOC_EXTENSIONS:
        return _make_id(str(resolved))
    root = _gdscript_project_root(source)
    if root is not None:
        try:
            return _make_id(_file_stem(resolved.relative_to(root)))
        except ValueError:
            pass
    return _make_id(str(resolved))


def extract_gdscript(path: Path) -> dict:
    """Extract classes, functions, signals, inherits, and preload/load imports from a .gd file.

    GDScript-specific handling:
      - class_name X     → file alias node (so external refs resolve by class_name)
      - extends Y        → inherits edge from file → Y
      - preload("res://...") / load("res://...")  → imports_from edge to target file
      - signal name(...) → signal node with contains edge
      - class Inner extends Base:  → nested class node with inherits edge
      - func name(...):  → function node with calls edges from its body
      - signal.emit(...) / signal.connect(callback)  → emits / connects edges
    """
    try:
        from tree_sitter_language_pack import get_parser
    except ImportError:
        # GDScript's grammar has no standalone tree-sitter-* wheel on PyPI, so
        # the only source is the (large) language pack. That is why it is an
        # optional extra rather than a core dependency: nobody who is not
        # writing Godot code should pay for ~150 grammars they never parse.
        # Name the exact command -- an error that only states what is missing
        # leaves the user to guess the extra's name.
        return {
            "nodes": [],
            "edges": [],
            "error": (
                "GDScript (.gd) support needs the optional Godot extra. "
                "Install it with:  pip install 'halal-graphify[godot]'  "
                "(.tscn/.tres scene files are parsed without it.)"
            ),
        }

    try:
        parser = get_parser("gdscript")
        source = path.read_bytes()
        tree = parser.parse(source)
        root = tree.root_node
    except Exception as e:
        return {"nodes": [], "edges": [], "error": str(e)}

    stem = path.stem
    str_path = str(path)
    nodes: list[dict] = []
    edges: list[dict] = []
    seen_ids: set[str] = set()
    function_bodies: list[tuple[str, Any]] = []
    # Signals defined in this file, keyed by simple name → node id
    signal_nids: dict[str, str] = {}

    def add_node(nid: str, label: str, line: int) -> None:
        if nid not in seen_ids:
            seen_ids.add(nid)
            nodes.append({
                "id": nid,
                "label": label,
                "file_type": "code",
                "source_file": str_path,
                "source_location": f"L{line}",
            })

    def add_edge(src: str, tgt: str, relation: str, line: int,
                 confidence: str = "EXTRACTED", weight: float = 1.0) -> None:
        edges.append({
            "source": src,
            "target": tgt,
            "relation": relation,
            "confidence": confidence,
            "source_file": str_path,
            "source_location": f"L{line}",
            "weight": weight,
        })

    file_nid = _make_id(str(path))
    add_node(file_nid, path.name, 1)

    def _resolve_inherits(base_name: str, line: int, src_nid: str) -> None:
        """Emit inherits edge. Base could be a class_name or a path-based reference."""
        # Strip "res://..." form (rare: extends "res://foo.gd")
        if base_name.startswith('"') and base_name.endswith('"'):
            raw = base_name.strip('"')
            resolved = _gdscript_resolve_res_path(raw, path)
            if resolved is not None:
                add_edge(src_nid, _resource_target_id(resolved, path), "inherits", line,
                         confidence="EXTRACTED")
                return
        # Bare identifier — class_name or built-in type (Node, RefCounted, etc.)
        tgt_nid = _make_id(base_name)
        # Create a stub node for the base so the edge survives _resolve_cross_file_imports
        if tgt_nid not in seen_ids:
            nodes.append({
                "id": tgt_nid,
                "label": base_name,
                "file_type": "code",
                "source_file": "",
                "source_location": "",
            })
            seen_ids.add(tgt_nid)
        add_edge(src_nid, tgt_nid, "inherits", line, confidence="EXTRACTED")

    def _extends_base_name(node) -> str | None:
        """Given an extends_statement, return the base name (identifier or string)."""
        for child in node.children:
            if child.type == "type":
                for sub in child.children:
                    if sub.type == "identifier":
                        return _read_text(sub, source)
            elif child.type == "string":
                return _read_text(child, source)
            elif child.type == "identifier":
                return _read_text(child, source)
        return None

    def _preload_target(call_node) -> Path | None:
        """If this call node is preload(...) or load(...) with a string literal, resolve target."""
        if not call_node.children:
            return None
        head = call_node.children[0]
        if head.type != "identifier":
            return None
        fn_name = _read_text(head, source)
        if fn_name not in ("preload", "load"):
            return None
        args = None
        for c in call_node.children:
            if c.type == "arguments":
                args = c
                break
        if args is None:
            return None
        for arg in args.children:
            if arg.type == "string":
                raw = _read_text(arg, source).strip('"\'')
                return _gdscript_resolve_res_path(raw, path)
        return None

    def _find_preloads(node) -> None:
        """Walk anywhere for preload()/load() calls and emit imports edges."""
        if node.type == "call":
            target = _preload_target(node)
            if target is not None:
                tgt_nid = _resource_target_id(target, path)
                line = node.start_point[0] + 1
                add_edge(file_nid, tgt_nid, "imports_from", line,
                         confidence="EXTRACTED")
        for child in node.children:
            _find_preloads(child)

    def walk(node, parent_class_nid: str | None, scope_nid: str) -> None:
        t = node.type
        line = node.start_point[0] + 1

        if t == "class_name_statement":
            name_node = node.child_by_field_name("name")
            if name_node:
                class_name = _read_text(name_node, source)
                alias_nid = _make_id(class_name)
                # class_name is a *file alias* — pointers to "MyClass" should hit the file node
                if alias_nid != file_nid and alias_nid not in seen_ids:
                    nodes.append({
                        "id": alias_nid,
                        "label": class_name,
                        "file_type": "code",
                        "source_file": str_path,
                        "source_location": f"L{line}",
                    })
                    seen_ids.add(alias_nid)
                    add_edge(file_nid, alias_nid, "aliases", line)
            return

        if t == "extends_statement":
            base = _extends_base_name(node)
            if base:
                # If we're inside an inner class body, inherit from that class; otherwise file-level
                tgt_src = parent_class_nid if parent_class_nid else file_nid
                _resolve_inherits(base, line, tgt_src)
            return

        if t == "signal_statement":
            name_node = node.child_by_field_name("name")
            if name_node:
                sig_name = _read_text(name_node, source)
                sig_nid = _make_id(stem, "signal", sig_name)
                add_node(sig_nid, f"{sig_name}(signal)", line)
                add_edge(scope_nid, sig_nid, "contains", line)
                signal_nids[sig_name] = sig_nid
            return

        if t == "class_definition":
            name_node = node.child_by_field_name("name")
            if not name_node:
                return
            class_name = _read_text(name_node, source)
            class_nid = _make_id(stem, class_name)
            add_node(class_nid, class_name, line)
            add_edge(scope_nid, class_nid, "contains", line)
            # extends_statement sits as a direct child
            for child in node.children:
                if child.type == "extends_statement":
                    base = _extends_base_name(child)
                    if base:
                        _resolve_inherits(base, child.start_point[0] + 1, class_nid)
            body = None
            for child in node.children:
                if child.type == "class_body":
                    body = child
                    break
            if body:
                for child in body.children:
                    walk(child, parent_class_nid=class_nid, scope_nid=class_nid)
            return

        if t in ("function_definition", "constructor_definition"):
            if t == "constructor_definition":
                func_name = "_init"
            else:
                name_node = node.child_by_field_name("name")
                if not name_node:
                    return
                func_name = _read_text(name_node, source)
            if parent_class_nid:
                func_nid = _make_id(parent_class_nid, func_name)
                add_node(func_nid, f".{func_name}()", line)
                add_edge(parent_class_nid, func_nid, "method", line)
            else:
                func_nid = _make_id(stem, func_name)
                add_node(func_nid, f"{func_name}()", line)
                add_edge(file_nid, func_nid, "contains", line)
            body = node.child_by_field_name("body")
            if body:
                function_bodies.append((func_nid, body))
            return

        # Default: recurse but preserve class context only for direct children of classes
        for child in node.children:
            walk(child, parent_class_nid=parent_class_nid, scope_nid=scope_nid)

    walk(root, parent_class_nid=None, scope_nid=file_nid)
    _find_preloads(root)

    # ── Call graph pass ──────────────────────────────────────────────────────
    # Build label index for local resolution
    label_to_nid: dict[str, str] = {}
    for n in nodes:
        raw = n.get("label", "")
        normalised = raw.strip("()").lstrip(".")
        # Strip "(signal)" suffix so emit/connect match by signal name alone
        if normalised.endswith("(signal)"):
            normalised = normalised[:-len("(signal)")].strip()
        if normalised:
            label_to_nid[normalised.lower()] = n["id"]

    seen_call_pairs: set[tuple[str, str, str]] = set()
    raw_calls: list[dict] = []

    def _parent_attribute_prev_ident(call_node, attribute_parent) -> str | None:
        """For attribute_call inside an attribute, find the named identifier/attribute_name
        that precedes this call_node (i.e. the 'object.method' pair)."""
        prev_name: str | None = None
        for c in attribute_parent.children:
            if c is call_node:
                return prev_name
            if c.type == "identifier":
                prev_name = _read_text(c, source)
            # for chained: EventBus.enemy_killed.emit(...) → attribute_parent holds
            # identifier, ., identifier, ., attribute_call — we want the last identifier
            # before the attribute_call
        return prev_name

    def walk_calls(node, caller_nid: str, parent=None) -> None:
        t = node.type
        # Boundary: don't recurse into nested function definitions
        if t in ("function_definition", "constructor_definition") and parent is not None:
            return

        if t in ("call", "attribute_call"):
            callee_name: str | None = None
            if node.children:
                head = node.children[0]
                if head.type == "identifier":
                    callee_name = _read_text(head, source)

            if callee_name:
                # emit/connect get special handling — the receiver is a signal, not the method
                if callee_name == "emit" and parent is not None and parent.type == "attribute":
                    sig_name = _parent_attribute_prev_ident(node, parent)
                    if sig_name:
                        sig_nid = signal_nids.get(sig_name) or label_to_nid.get(sig_name.lower())
                        if sig_nid and sig_nid != caller_nid:
                            key = (caller_nid, sig_nid, "emits")
                            if key not in seen_call_pairs:
                                seen_call_pairs.add(key)
                                add_edge(caller_nid, sig_nid, "emits",
                                         node.start_point[0] + 1)
                elif callee_name == "connect" and parent is not None and parent.type == "attribute":
                    # First argument — identifier that names the callback method
                    args = None
                    for c in node.children:
                        if c.type == "arguments":
                            args = c
                            break
                    callback_name: str | None = None
                    if args:
                        for arg in args.children:
                            if arg.type == "identifier":
                                callback_name = _read_text(arg, source)
                                break
                    sig_name = _parent_attribute_prev_ident(node, parent)
                    if sig_name and callback_name:
                        sig_nid = signal_nids.get(sig_name) or label_to_nid.get(sig_name.lower())
                        cb_nid = label_to_nid.get(callback_name.lower())
                        line = node.start_point[0] + 1
                        if sig_nid and cb_nid and sig_nid != cb_nid:
                            key = (sig_nid, cb_nid, "connected_to")
                            if key not in seen_call_pairs:
                                seen_call_pairs.add(key)
                                add_edge(sig_nid, cb_nid, "connected_to", line)
                        elif sig_nid and callback_name:
                            # Callback not resolved locally — defer
                            raw_calls.append({
                                "caller_nid": sig_nid,
                                "callee": callback_name,
                                "source_file": str_path,
                                "source_location": f"L{line}",
                            })
                else:
                    tgt_nid = label_to_nid.get(callee_name.lower())
                    line = node.start_point[0] + 1
                    if tgt_nid and tgt_nid != caller_nid:
                        key = (caller_nid, tgt_nid, "calls")
                        if key not in seen_call_pairs:
                            seen_call_pairs.add(key)
                            add_edge(caller_nid, tgt_nid, "calls", line)
                    elif callee_name and callee_name not in ("preload", "load"):
                        raw_calls.append({
                            "caller_nid": caller_nid,
                            "callee": callee_name,
                            "source_file": str_path,
                            "source_location": f"L{line}",
                        })

        for child in node.children:
            walk_calls(child, caller_nid, parent=node)

    for caller_nid, body_node in function_bodies:
        # Walk children directly so we don't stop at the body itself
        for child in body_node.children:
            walk_calls(child, caller_nid, parent=body_node)

    clean_edges = [
        e for e in edges
        if e["source"] in seen_ids and (
            e["target"] in seen_ids or
            e["relation"] in ("imports", "imports_from", "inherits")
        )
    ]
    return {"nodes": nodes, "edges": clean_edges, "raw_calls": raw_calls}


# ── Godot scene/resource extractor (regex, no tree-sitter) ───────────────────
#
# Godot .tscn (scene) and .tres (resource) files share a simple, line-oriented
# format. We extract:
#   - ext_resource paths → imports_from edges to the target file
#   - [node ...] script = ExtResource("id") → script attachment (subset of
#     imports_from, already captured via ext_resource)
#   - [node ... instance=ExtResource("id")] → scene instancing (imports_from)
#   - [connection signal="..." from=X to=Y method=M] → connected_to edge
#     (deferred as raw_call so the cross-file resolver can wire it to the
#     target method node)
#
# Regex rather than a full parser is intentional: Godot's serializer emits
# deterministic, line-per-attribute formatting, and we only need a handful of
# fields. For structural fidelity on nested sub_resources we'd need a real
# parser, but those don't create cross-file edges so the cost isn't worth it.


_TSCN_SECTION_RE = re.compile(r'^\s*\[([a-z_]+)\b([^\]]*)\]\s*$')
_TSCN_ATTR_RE = re.compile(r'(\w+)\s*=\s*"([^"]*)"')
_TSCN_SCRIPT_ASSIGN_RE = re.compile(r'^\s*script\s*=\s*ExtResource\s*\(\s*"?([^")]+)"?\s*\)')
_TSCN_INSTANCE_RE = re.compile(r'instance\s*=\s*ExtResource\s*\(\s*"?([^")]+)"?\s*\)')


def extract_gd_scene(path: Path) -> dict:
    """Extract cross-file edges from a Godot .tscn (scene) or .tres (resource) file.

    Emits a file node plus imports_from edges for every ext_resource, and
    connects_to entries (deferred) for [connection] sections so the global
    resolver can wire them to the target script's method nodes.
    """
    str_path = str(path)
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return {"nodes": [], "edges": [], "error": str(e)}

    nodes: list[dict] = []
    edges: list[dict] = []
    seen_ids: set[str] = set()
    raw_calls: list[dict] = []

    def add_node(nid: str, label: str, line: int) -> None:
        if nid not in seen_ids:
            seen_ids.add(nid)
            nodes.append({
                "id": nid,
                "label": label,
                "file_type": "code",
                "source_file": str_path,
                "source_location": f"L{line}",
            })

    def add_edge(src: str, tgt: str, relation: str, line: int,
                 confidence: str = "EXTRACTED", weight: float = 1.0) -> None:
        edges.append({
            "source": src,
            "target": tgt,
            "relation": relation,
            "confidence": confidence,
            "source_file": str_path,
            "source_location": f"L{line}",
            "weight": weight,
        })

    file_nid = _make_id(str(path))
    add_node(file_nid, path.name, 1)

    # id → resolved Path cache for ext_resource references
    ext_res: dict[str, Path] = {}
    ext_res_line: dict[str, int] = {}

    # Resolve res:// using the shared helper from the GDScript extractor
    def _resolve(raw: str) -> Path | None:
        return _gdscript_resolve_res_path(raw, path)

    cur_section: str | None = None
    cur_section_attrs: dict[str, str] = {}
    cur_section_line = 0

    for lineno, line in enumerate(text.splitlines(), start=1):
        m = _TSCN_SECTION_RE.match(line)
        if m:
            cur_section = m.group(1)
            cur_section_attrs = dict(_TSCN_ATTR_RE.findall(m.group(2)))
            cur_section_line = lineno

            if cur_section == "ext_resource":
                path_str = cur_section_attrs.get("path", "")
                res_id = cur_section_attrs.get("id", "")
                if path_str:
                    resolved = _resolve(path_str)
                    if resolved is not None:
                        tgt_nid = _resource_target_id(resolved, path)
                        add_edge(file_nid, tgt_nid, "imports_from", lineno)
                        if res_id:
                            ext_res[res_id] = resolved
                            ext_res_line[res_id] = lineno

            elif cur_section == "node":
                # Node instancing via instance=ExtResource("id") in the header attrs
                instance_match = _TSCN_INSTANCE_RE.search(line)
                if instance_match:
                    ref_id = instance_match.group(1)
                    target = ext_res.get(ref_id)
                    if target is not None:
                        tgt_nid = _resource_target_id(target, path)
                        # Edge already exists (from ext_resource), skip duplicate —
                        # but emit an "instances" edge for semantic distinctness
                        add_edge(file_nid, tgt_nid, "instances", lineno)

            elif cur_section == "connection":
                signal_name = cur_section_attrs.get("signal", "")
                method_name = cur_section_attrs.get("method", "")
                # Defer as raw_call so the global resolver wires it to the method
                # node when it exists anywhere in the corpus.
                if method_name:
                    raw_calls.append({
                        "caller_nid": file_nid,
                        "callee": method_name,
                        "source_file": str_path,
                        "source_location": f"L{lineno}",
                    })
                # Also try to connect to a signal node by name (from the GDScript
                # extractor's naming: "<stem>_signal_<name>"). Labels are indexed
                # globally in extract() so a raw_call on the signal name would
                # resolve to a local function with the same name too — risky. We
                # rely on the resolver matching the method_name only.
            continue

        # Inside a section: look for script = ExtResource("...") — doesn't add
        # new edges beyond ext_resource, but we note the binding for clarity.
        if cur_section in ("node", "resource"):
            sm = _TSCN_SCRIPT_ASSIGN_RE.match(line)
            if sm:
                ref_id = sm.group(1)
                target = ext_res.get(ref_id)
                if target is not None:
                    # Already have imports_from on the file; no-op for now.
                    pass

    return {"nodes": nodes, "edges": edges, "raw_calls": raw_calls}


def extract_tscn(path: Path) -> dict:
    """Extract cross-file edges from a Godot .tscn scene file."""
    return extract_gd_scene(path)


def extract_tres(path: Path) -> dict:
    """Extract cross-file edges from a Godot .tres resource file."""
    return extract_gd_scene(path)
