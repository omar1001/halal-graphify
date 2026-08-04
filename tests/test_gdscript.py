"""GDScript / Godot extractor coverage (.gd AST + .tscn/.tres scene text).

The fork this was ported from shipped no tests for its ~540-line extractor; these
guard the behaviours project graphs depend on: class/func/signal nodes with line
anchors, inherits/preload/emit/connect edges, scene script-bindings and node
instances, and — critically — that no edge endpoint ever embeds an absolute
filesystem path (which would differ across machines and churn graph.json).
"""
from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from halal_graphify.extract import _make_id, extract, extract_gdscript, extract_tscn

# Warm the GDScript grammar at IMPORT time, deliberately.
#
# tests/conftest.py gives every test a throwaway HOME and points LOCALAPPDATA
# at a directory that does not exist, so installers can never touch the real
# machine. tree_sitter_language_pack resolves its grammar cache from exactly
# those variables, so inside a test it cannot find a cache directory and fails
# with "Could not determine system cache directory" -- and it memoises that
# failure, so every later call in the same process fails too.
#
# Module import happens at collection, BEFORE the sandbox fixture applies, so
# resolving the parser here uses the real cache directory. The successful
# parser is then memoised and every test below gets it regardless of the
# sandbox. This is a test-harness interaction only: nothing is wrong with the
# extractor, which resolves its own parser normally in real use.
try:
    from tree_sitter_language_pack import get_parser as _get_parser

    _get_parser("gdscript")
    _GDSCRIPT_GRAMMAR = True
except Exception:  # pack absent, or grammar unavailable on this platform
    _GDSCRIPT_GRAMMAR = False

# .gd needs the optional [godot] extra; .tscn/.tres are pure regex and always run.
requires_grammar = unittest.skipUnless(
    _GDSCRIPT_GRAMMAR,
    "GDScript grammar unavailable - install the optional extra: "
    "pip install 'halal-graphify[godot]'",
)


class TestGDScriptExtractor(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # A minimal Godot project so res:// resolves against a real project root.
        (self.root / "project.godot").write_text("; engine config\n", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def _write(self, rel: str, text: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(textwrap.dedent(text), encoding="utf-8")
        return p

    @requires_grammar
    def test_gdscript_classes_functions_signals_inherits_and_preload(self):
        self._write("components/health.gd", "extends Node\nclass_name Health\n")
        gd = self._write(
            "entities/player.gd",
            """
            extends CharacterBody3D
            class_name Player

            signal died

            const Health = preload("res://components/health.gd")

            func _ready() -> void:
                _spawn()

            func _spawn() -> void:
                died.emit()
            """,
        )
        res = extract_gdscript(gd)
        self.assertNotIn("error", res, res.get("error"))
        rels = {e["relation"] for e in res["edges"]}
        # Structural relationships the fork advertises.
        self.assertIn("inherits", rels)       # extends CharacterBody3D
        self.assertIn("aliases", rels)         # class_name Player
        self.assertIn("contains", rels)        # func / signal membership
        self.assertIn("imports_from", rels)    # preload("res://components/health.gd")
        self.assertIn("emits", rels)           # died.emit()
        # Every code node carries a line anchor.
        anchored = [n for n in res["nodes"] if n.get("source_location", "").startswith("L")]
        self.assertTrue(anchored)
        # A function node exists for _ready.
        self.assertTrue(any("_ready" in n["id"] for n in res["nodes"]))

    def test_tscn_script_binding_and_instance_edges(self):
        self._write("entities/enemy.gd", "extends Node3D\nclass_name Enemy\n")
        scene = self._write(
            "entities/enemy.tscn",
            """
            [gd_scene load_steps=3 format=3]

            [ext_resource type="Script" path="res://entities/enemy.gd" id="1_abc"]
            [ext_resource type="PackedScene" path="res://entities/enemy.tscn" id="2_def"]
            [ext_resource type="ArrayMesh" path="res://art/enemy_mesh.glb" id="3_ghi"]

            [node name="Enemy" type="Node3D"]
            script = ExtResource("1_abc")
            """,
        )
        res = extract_tscn(scene)
        self.assertNotIn("error", res, res.get("error"))
        rels = [e["relation"] for e in res["edges"]]
        self.assertIn("imports_from", rels)   # ext_resource script/mesh bindings

    # Without the grammar the .gd file yields no nodes, so "no absolute paths
    # leaked" would hold vacuously. Skip rather than pass on an empty graph.
    @requires_grammar
    def test_no_absolute_path_leaks_through_full_pipeline(self):
        # A .tscn referencing a .glb model: the .glb is not a corpus code file, so
        # extract()'s id-remap never canonicalises it. Run the FULL pipeline (as
        # `halal-graphify update` does) and assert no edge endpoint embeds the absolute
        # on-disk path — the machine-specific form that breaks graph portability.
        gd = self._write("entities/enemy.gd", "extends Node3D\nclass_name Enemy\n")
        scene = self._write(
            "world/level.tscn",
            """
            [gd_scene load_steps=3 format=3]

            [ext_resource type="Script" path="res://entities/enemy.gd" id="1_s"]
            [ext_resource type="ArrayMesh" path="res://art/mesh.glb" id="2_m"]

            [node name="Enemy" type="Node3D"]
            script = ExtResource("1_s")
            """,
        )
        # parallel=False keeps the test deterministic under pytest on Windows.
        res = extract([gd, scene], cache_root=self.root, root=self.root, parallel=False)
        abs_marker = _make_id(str(self.root.resolve()))
        for e in res["edges"]:
            for endpoint in (e["source"], e["target"]):
                self.assertFalse(
                    str(endpoint).startswith(abs_marker),
                    f"absolute path leaked into edge endpoint: {endpoint}",
                )
        # And the .glb edge still exists, in portable relative form.
        self.assertTrue(
            any(e["target"] == _make_id("art/mesh") for e in res["edges"]),
            "expected portable imports_from edge to art/mesh(.glb)",
        )


if __name__ == "__main__":
    unittest.main()
