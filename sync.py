"""Regenerate halal-graphify from upstream's newest release.

There is no `git merge` anywhere in this file, and that is the whole design.
The fork's tree is thrown away and rebuilt from an upstream tag on every sync,
so a resync cannot produce a merge conflict -- there is nothing to conflict
with. The cost is that the fork does not carry upstream's commit history; the
benefit is that this never needs a human to resolve anything.

Two upstream quirks this has to work around, both verified the hard way:

  * `main` is stale. It sits at 0.1.14 while releases are at 0.9.x. Releases
    ship from versioned branches (v1 ... v8). Do not track `main`.

  * Tags are NOT monotonic. `v1.0.0` exists and looks newest, but points at an
    old tree whose pyproject says 0.1.10 -- 38 releases behind v0.9.32. Sorting
    tags by version number silently downgrades the fork. PyPI is the authority
    on what upstream actually shipped, so that is what we ask.

Usage:
    python sync.py            # sync to upstream's newest release, if any
    python sync.py --check    # report only, change nothing
    python sync.py --tag vX   # pin to a specific upstream tag
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPSTREAM = "https://github.com/Graphify-Labs/graphify"
UPSTREAM_DIST = "graphifyy"          # upstream's name on PyPI
FORK_PKG = "halal_graphify"

# Records which upstream tag the current tree was generated from.
UPSTREAM_TAG_FILE = "upstream-tag.txt"

# Files and directories that belong to the fork and must survive a
# regeneration. Everything else in the repo is generated and replaced wholesale.
FORK_OWNED = {
    ".git", ".github", "overlay",
    "rename.py", "sync.py",
    "update.bat", "migrate.bat",
    "fork-divergences.txt", "CLAUDE.md",
    ".gitignore", ".gitattributes", UPSTREAM_TAG_FILE,
}

# Fork-owned files inside a directory upstream also uses, so the directory
# itself cannot simply be listed above. These are carried across by hand.
FORK_OWNED_NESTED = {
    "docs/CHANGELOG.md",
}


def run(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    proc = subprocess.run(args, cwd=cwd, check=False,
                          capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(args)}\n{proc.stderr}")
    return proc.stdout.strip()


def _semver(tag: str) -> tuple[int, ...] | None:
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", tag)
    return tuple(int(g) for g in m.groups()) if m else None


def _upstream_tags() -> set[str]:
    """Every semver tag upstream. Peeled refs (`^{}`) are skipped so a tag is
    not counted twice."""
    out = run("git", "ls-remote", "--tags", UPSTREAM)
    tags = set()
    for line in out.splitlines():
        if "\t" not in line or line.endswith("^{}"):
            continue
        name = line.split("refs/tags/", 1)[-1]
        if _semver(name):
            tags.add(name)
    return tags


def newest_upstream_tag() -> str:
    """The tag of upstream's newest ACTUAL release.

    Do NOT "simplify" this back to max(semver over tags). See the module
    docstring: v1.0.0 is a stale tag that would win that comparison and roll
    the fork back by 38 releases.
    """
    tags = _upstream_tags()
    if not tags:
        raise SystemExit("no semver tags found upstream")

    try:
        with urllib.request.urlopen(
            f"https://pypi.org/pypi/{UPSTREAM_DIST}/json", timeout=30
        ) as resp:
            version = json.load(resp)["info"]["version"]
    except Exception as exc:                                   # noqa: BLE001
        raise SystemExit(
            f"could not reach PyPI to determine upstream's latest release: {exc}\n"
            "Refusing to guess from tag names, which are not monotonic here.\n"
            "Re-run later, or pin explicitly with --tag."
        ) from exc

    for candidate in (f"v{version}", version):
        if candidate in tags:
            return candidate
    raise SystemExit(
        f"PyPI reports {UPSTREAM_DIST} {version}, but upstream has no matching "
        f"tag. Check why, then pin explicitly with --tag."
    )


def current_fork_tag() -> str | None:
    """Read the recorded upstream tag rather than inferring it from the fork's
    own git tags. Inferring would hit the same non-monotonic trap: once v1.0.0
    has been tagged here, max(semver) reports it forever and every later sync
    looks like a no-op."""
    state = HERE / UPSTREAM_TAG_FILE
    return state.read_text(encoding="utf-8").strip() if state.is_file() else None


def _register_migrate_verb(main_py: Path) -> None:
    """Wire `halal-graphify migrate` into the CLI.

    Injected rather than added to upstream's dispatch table, because that
    table's shape is upstream's to change. Intercepting before dispatch is
    stable across upstream refactors.
    """
    text = main_py.read_text(encoding="utf-8")
    if "_hg_migrate_hook" in text:
        return

    hook = (
        "# --- halal-graphify addition ------------------------------------------\n"
        "# `migrate` is a fork-only verb. Intercepted here rather than added to\n"
        "# upstream's dispatch table so that regenerating against a new upstream\n"
        "# release cannot collide with changes to that table's shape.\n"
        "def _hg_migrate_hook():\n"
        "    import sys\n"
        "    if len(sys.argv) > 1 and sys.argv[1] == 'migrate':\n"
        "        from halal_graphify.migrate import main as _m\n"
        "        raise SystemExit(_m(sys.argv[2:]))\n"
        "\n\n"
    )

    # The definition must go BEFORE `def main(`, not at the end of the file:
    # __main__.py calls main() at module level, which runs before anything
    # appended after that call has been defined.
    pattern = re.compile(
        r"(?m)^(def main\([^)]*\)[^:]*:\n)((?:[ \t]+(?:\"\"\".*?\"\"\"|'''.*?''')\n)?)",
        re.DOTALL,
    )
    m = pattern.search(text)
    if not m:
        raise SystemExit("could not find `def main(` in __main__.py to wire `migrate` into")

    # The call goes after main()'s docstring, so the docstring stays a docstring.
    text = (text[:m.start()] + hook + m.group(1) + m.group(2)
            + "    _hg_migrate_hook()\n" + text[m.end():])
    main_py.write_text(text, encoding="utf-8")


def _anchored_insert(text: str, anchor: str, addition: str, *, what: str,
                     where: str) -> str:
    """Insert `addition` immediately after the line containing `anchor`.

    Fails loud rather than silently doing nothing: a missing anchor means
    upstream moved the thing we hook into, and a silently skipped patch would
    ship a release whose Godot support is quietly half-wired. Idempotent --
    if the addition is already present the text is returned untouched, so a
    re-run cannot duplicate it.
    """
    if addition.strip() in text:
        return text
    if anchor not in text:
        raise SystemExit(
            f"\nGodot overlay: could not find the {what} anchor in {where}.\n"
            f"  looked for: {anchor.strip()[:100]}\n"
            "Upstream has moved or rewritten it. Update the anchor in sync.py\n"
            "(_install_gdscript_extractor). Nothing has been published."
        )
    line_end = text.index(anchor) + len(anchor)
    line_end = text.index("\n", line_end) + 1
    return text[:line_end] + addition + text[line_end:]


def _install_gdscript_extractor(src: Path) -> None:
    """Add Godot/GDScript support to the regenerated tree.

    Upstream Graphify has no GDScript backend at all -- .gd files fall through
    to `unclassified`, so a Godot project graphs to nothing useful. This wires
    in the fork's own extractor (overlay/gdscript.py), ported from Bruno
    Hidalgo's graphify-godot.

    Everything here is an ANCHORED INSERT into upstream's tables rather than a
    rewrite of them, for the same reason `migrate` is intercepted rather than
    added to the dispatch table: the tables' shape is upstream's to change, and
    an additive patch survives most refactors. Where an anchor does vanish, the
    build stops loudly instead of shipping a half-wired release.

    The grammar is an OPTIONAL extra (`[godot]`): GDScript has no standalone
    tree-sitter-* wheel on PyPI, so the only source is the large
    tree-sitter-language-pack, and making it a core dependency would tax every
    install for a language most users never touch. .tscn/.tres are pure regex
    and work with no extra at all.
    """
    pkg = src / FORK_PKG

    # 1. The extractor itself, and its tests.
    shutil.copy2(HERE / "overlay" / "gdscript.py", pkg / "extractors" / "gdscript.py")
    tests_dir = src / "tests"
    if tests_dir.is_dir():
        shutil.copy2(HERE / "overlay" / "test_gdscript.py", tests_dir / "test_gdscript.py")

    # 2. detect.py -- teach the scanner that .gd/.tscn/.tres are code, not
    #    unclassified junk. Without this the extractor is never reached.
    detect = pkg / "detect.py"
    text = detect.read_text(encoding="utf-8")
    if "'.gd'" not in text:
        anchor = "'.cls', '.trigger'}"
        if anchor not in text:
            raise SystemExit(
                "\nGodot overlay: CODE_EXTENSIONS tail not found in detect.py.\n"
                "Update the anchor in sync.py. Nothing has been published."
            )
        text = text.replace(anchor, "'.cls', '.trigger', '.gd', '.tscn', '.tres'}")
        detect.write_text(text, encoding="utf-8")

    # 3. extract.py -- import, extension->language map, extension->function
    #    dispatch. All three are needed; any one alone is a no-op.
    extract = pkg / "extract.py"
    text = extract.read_text(encoding="utf-8")
    text = _anchored_insert(
        text,
        f"from {FORK_PKG}.extractors.zig import extract_zig  # noqa: F401",
        f"from {FORK_PKG}.extractors.gdscript import "
        "extract_gdscript, extract_gd_scene, extract_tscn, extract_tres  # noqa: F401\n",
        what="extractor-import", where="extract.py",
    )
    text = _anchored_insert(
        text,
        '".ps1": "powershell", ".psm1": "powershell", ".psd1": "powershell",',
        '    ".gd": "gdscript", ".tscn": "gdscript", ".tres": "gdscript",\n',
        what="extension->language map", where="extract.py",
    )
    text = _anchored_insert(
        text,
        '    ".sql": extract_sql,',
        '    ".gd": extract_gdscript,\n'
        '    ".tscn": extract_tscn,\n'
        '    ".tres": extract_tres,\n',
        what="extension->extractor dispatch", where="extract.py",
    )
    extract.write_text(text, encoding="utf-8")

    # 4. extractors/__init__.py -- the by-language registry.
    init = pkg / "extractors" / "__init__.py"
    text = init.read_text(encoding="utf-8")
    text = _anchored_insert(
        text,
        f"from {FORK_PKG}.extractors.zig import extract_zig",
        f"from {FORK_PKG}.extractors.gdscript import "
        "extract_gdscript, extract_tres, extract_tscn\n",
        what="registry import", where="extractors/__init__.py",
    )
    text = _anchored_insert(
        text,
        '    "fortran": extract_fortran,',
        '    "gdscript": extract_gdscript,\n'
        '    "tscn": extract_tscn,\n'
        '    "tres": extract_tres,\n',
        what="LANGUAGE_EXTRACTORS registry", where="extractors/__init__.py",
    )
    init.write_text(text, encoding="utf-8")

    # 5. pyproject.toml -- the optional extra, plus membership of `all`.
    pyproject = src / "pyproject.toml"
    text = pyproject.read_text(encoding="utf-8")
    if "godot = [" not in text:
        anchor = 'terraform = ["tree-sitter-hcl"]'
        if anchor not in text:
            raise SystemExit(
                "\nGodot overlay: optional-extras block not found in pyproject.toml.\n"
                "Update the anchor in sync.py. Nothing has been published."
            )
        text = text.replace(anchor, anchor + "\n" + (
            "# GDScript has no standalone tree-sitter-* wheel on PyPI; the language\n"
            "# pack (PrestonKnopp/tree-sitter-gdscript) is the only source, and it is\n"
            "# large. Optional so only Godot users pay for it. .tscn/.tres need nothing.\n"
            'godot = ["tree-sitter-language-pack>=0.9"]'
        ))
    # The leading comma matters: a bare '"tree-sitter-pascal"]' also matches
    # `pascal = ["tree-sitter-pascal"]` two lines up and would quietly drag the
    # language pack into the pascal extra as well. Only the `all` list has a
    # preceding element, so only it has the comma.
    if "tree-sitter-language-pack" not in text.split("all = [")[1].split("]")[0]:
        text = text.replace(', "tree-sitter-pascal"]',
                            ', "tree-sitter-pascal", "tree-sitter-language-pack"]')
    pyproject.write_text(text, encoding="utf-8")

    # 6. README -- listed alongside the other languages, deliberately NOT
    #    promoted to the banner or the intro. Godot is an inclusion here, not
    #    the fork's headline; the headline is still the renamed term.
    readme = src / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = _anchored_insert(
        text,
        "| `pascal` | Pascal / Delphi",
        "| `godot` | Godot GDScript `.gd` AST extraction "
        "(`.tscn`/`.tres` scene files are parsed without it) | "
        '`uv tool install "halal-graphify[godot]"` |\n',
        what="optional-extras table row", where="README.md",
    )
    text = _anchored_insert(
        text,
        "| Terraform / HCL | `.tf .tfvars .hcl`",
        "| Godot / GDScript | `.gd` (classes, functions, signals, `extends`, "
        "`preload`/`load`, `emit`/`connect`; requires "
        "`uv tool install halal-graphify[godot]`) and `.tscn .tres` scene/resource "
        "files (script bindings and instanced scenes, no extra needed) |\n",
        what="file-types table row", where="README.md",
    )
    readme.write_text(text, encoding="utf-8")

    # 7. NOTICE -- Apache-2.0 s4(d) attribution for the ported GDScript code.
    #    LICENSE itself is copied verbatim and never touched; NOTICE is the
    #    correct place to record a derived component's provenance.
    notice = src / "NOTICE"
    text = notice.read_text(encoding="utf-8")
    if "GDScript" not in text:
        text = text.rstrip("\n") + "\n\n" + (
            "The GDScript / Godot extractor (halal_graphify/extractors/gdscript.py)\n"
            "is not part of upstream Graphify. It derives from the graphify-godot\n"
            "fork by Bruno Hidalgo (MIT), ported onto Graphify v0.9.23 by Epic\n"
            "Millennium, and is carried here as a fork-owned overlay.\n"
        )
        notice.write_text(text, encoding="utf-8")


def regenerate(tag: str, workdir: Path) -> Path:
    """Fetch the tag, transform it, and return the generated tree."""
    src = workdir / "upstream"
    print(f"  fetching {tag} ...")
    run("git", "clone", "--quiet", "--depth", "1", "--branch", tag, UPSTREAM, str(src))
    shutil.rmtree(src / ".git", ignore_errors=True)

    print("  applying rename ...")
    proc = subprocess.run([sys.executable, str(HERE / "rename.py"), str(src)],
                          check=False, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            "\nThe rename guard failed, so nothing has been published.\n"
            "Upstream has most likely introduced a spelling the transform does\n"
            "not cover. Fix overlay/migrate.py, then re-run."
        )

    # The overlay: fork-only files that must NOT go through rename.py.
    print("  applying overlay ...")
    shutil.copy2(HERE / "overlay" / "migrate.py", src / FORK_PKG / "migrate.py")
    _register_migrate_verb(src / FORK_PKG / "__main__.py")
    _install_gdscript_extractor(src)
    return src


def swap_tree(generated: Path) -> None:
    """Replace the fork's generated content, preserving what the fork owns."""
    stashed: dict[str, bytes] = {}
    for rel in FORK_OWNED_NESTED:
        p = HERE / rel
        if p.is_file():
            stashed[rel] = p.read_bytes()

    for entry in HERE.iterdir():
        if entry.name in FORK_OWNED:
            continue
        if entry.is_dir():
            shutil.rmtree(entry, ignore_errors=True)
        else:
            entry.unlink()

    for entry in generated.iterdir():
        if entry.name in FORK_OWNED:
            continue
        dst = HERE / entry.name
        if entry.is_dir():
            shutil.copytree(entry, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(entry, dst)

    for rel, data in stashed.items():
        p = HERE / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report whether a newer release exists; change nothing")
    ap.add_argument("--tag", help="pin to a specific upstream tag")
    ap.add_argument("--no-commit", action="store_true", help="leave changes uncommitted")
    args = ap.parse_args(argv)

    target = args.tag or newest_upstream_tag()
    current = current_fork_tag()
    print(f"upstream newest: {target}")
    print(f"fork currently:  {current or '(none)'}")

    if args.check:
        print("update available" if target != current else "up to date")
        return 0

    if target == current and not args.tag:
        print("Already up to date. Nothing to do.")
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        generated = regenerate(target, Path(tmp))
        print("  swapping tree ...")
        swap_tree(generated)

    (HERE / UPSTREAM_TAG_FILE).write_text(target + "\n", encoding="utf-8")

    # Apache-2.0 §4a: a redistribution must carry the licence. If a tag's tree
    # lacks them, something is wrong with that tag -- stop rather than ship.
    missing = [f for f in ("LICENSE", "NOTICE") if not (HERE / f).is_file()]
    if missing:
        raise SystemExit(
            f"refusing to publish: {', '.join(missing)} missing from the generated tree"
        )

    if args.no_commit:
        print(f"\nDone (uncommitted). Review, then tag as {target}.")
        return 0

    run("git", "add", "-A", cwd=HERE)
    if not run("git", "status", "--porcelain", cwd=HERE, check=False):
        print("Tree identical to what is already committed. Nothing to do.")
        return 0

    run("git", "commit", "-q", "-m",
        f"sync: upstream {target} -> halal-graphify {target.lstrip('v')}", cwd=HERE)
    run("git", "tag", "-f", target, cwd=HERE)
    print(f"\nCommitted and tagged {target}. Push with:  git push --follow-tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
