"""Convert projects that still use the upstream Graphify terminology.

=============================================================================
 THIS FILE IS THE ONLY PLACE IN halal-graphify WHERE THE OLD TERM APPEARS.
=============================================================================

That is deliberate, and it is not an oversight to be "cleaned up".

halal-graphify exists to remove one word from Graphify's vocabulary. A tool
that removes a word must contain that word in order to search for it -- the
same way a profanity filter must contain the list it blocks. So the term is
quarantined here, in the single module whose entire purpose is deleting it
from other people's projects.

Everywhere else in this package the term does not appear, is never accepted as
input, and is never shown to a user. ``rename.py`` enforces that mechanically
on every sync and imports its vocabulary from this file, so the two can never
drift apart.

We deliberately did NOT obfuscate the term (building it from fragments at
runtime to defeat ``grep``). That would have produced a clean grep and
misleading code. Honest and quarantined beats hidden.

If you are reading this because a linter or a well-meaning contributor flagged
the file: please leave it exactly as it is.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# The vocabulary. Single source of truth, imported by rename.py.
# --------------------------------------------------------------------------

OLD_TERM = "god"
NEW_TERM = "hub"

# Words that CONTAIN the old term but have nothing to do with it. These must
# survive untouched. Renaming them would corrupt unrelated text.
#
# `tygodnie` is not hypothetical: it is Polish for "weeks" and appears in
# upstream's own docs/translations/README.pl-PL.md. A naive substring replace
# turns it into "tyhubnie" and quietly mangles the Polish translation.
PROTECTED_WORDS = frozenset({
    "tygodnie",     # pl: "weeks"     - present in upstream translations today
    "tygodnia",     # pl: "week"      - inflected form
    "godzin",       # pl/uk: "hours"  - stem, covers godzina/godziny/godzinach
    "godina",       # hr/sr/bg: "year"
    "godot",        # the game engine - plausible future tree-sitter language
    "gdscript",     # (no match, listed for the reader's benefit)
    "pagoda",       # en
    "pagodas",
})

# Structural keys written by graphify into its own output files. Only these
# are renamed during data migration. Everything else in a graph -- node ids,
# labels, file paths -- is the USER's own source code and is never touched.
#
# This matters: a user whose codebase contains a function named `god_mode`
# would have their graph corrupted by a blind text replace.
JSON_KEY_MAP = {
    "gods": "hubs",
    "god_nodes": "hub_nodes",
    "god_nodes_data": "hub_nodes_data",
    "gods_data": "hubs_data",
    "god_set": "hub_set",
    "god_articles": "hub_articles",
    "god_node_list": "hub_node_list",
}

# Files inside an output directory that are fully machine-generated, so a text
# swap on them is safe (no user prose to damage).
GENERATED_REPORT_NAMES = {"GRAPH_REPORT.md", "GRAPH_REPORT.html", "index.md"}

DOC_SUFFIXES = {".md", ".txt", ".json", ".toml", ".yml", ".yaml", ".py", ".html", ".svg"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".mypy_cache"}


# --------------------------------------------------------------------------
# The transform
# --------------------------------------------------------------------------

def _build_pattern() -> re.Pattern:
    """Protected words are listed first so the alternation matches them whole
    and hands them back unchanged, before the bare term can match inside."""
    alts = sorted(PROTECTED_WORDS, key=len, reverse=True)
    return re.compile("|".join([*(re.escape(w) for w in alts), OLD_TERM]), re.IGNORECASE)


_PATTERN = _build_pattern()
_PROTECTED_LOWER = {w.lower() for w in PROTECTED_WORDS}


def swap_term(text: str) -> str:
    """Replace the old term with the new one, preserving case, skipping
    protected words. `god`->`hub`, `God`->`Hub`, `GOD`->`HUB`."""

    def repl(m: re.Match) -> str:
        s = m.group(0)
        if s.lower() in _PROTECTED_LOWER:
            return s
        if s.isupper():
            return NEW_TERM.upper()
        if s[0].isupper():
            return NEW_TERM.capitalize()
        return NEW_TERM

    return _PATTERN.sub(repl, text)


def remaining_hits(text: str) -> list[str]:
    """Occurrences of the old term that are NOT protected words. Used by
    rename.py's guard and by this tool to decide whether work remains."""
    out = []
    for m in _PATTERN.finditer(text):
        if m.group(0).lower() not in _PROTECTED_LOWER:
            out.append(m.group(0))
    return out


def migrate_json_keys(obj):
    """Recursively rename structural keys only. Values are never touched."""
    changed = 0
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            nk = JSON_KEY_MAP.get(k, k)
            if nk != k:
                changed += 1
            nv, c = migrate_json_keys(v)
            changed += c
            new[nk] = nv
        return new, changed
    if isinstance(obj, list):
        out = []
        for item in obj:
            ni, c = migrate_json_keys(item)
            changed += c
            out.append(ni)
        return out, changed
    return obj, changed


# --------------------------------------------------------------------------
# File walking
# --------------------------------------------------------------------------

def _iter_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() not in DOC_SUFFIXES:
            continue
        yield p


def _read(p: Path) -> str | None:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None  # binary or unreadable - never touch


def _backup_and_write(p: Path, content: str, *, backup: bool) -> None:
    if backup:
        bak = p.with_suffix(p.suffix + ".bak")
        if not bak.exists():
            shutil.copy2(p, bak)
    p.write_text(content, encoding="utf-8")


def _find_output_dirs(root: Path) -> list[Path]:
    """Locate graphify output directories. The default name is kept identical
    to upstream on purpose, so halal-graphify reads graphs you already have."""
    hits = [d for d in root.rglob("graphify-out*") if d.is_dir()]
    if (root / "graph.json").exists() or (root / "analysis.json").exists():
        hits.append(root)
    return hits


# --------------------------------------------------------------------------
# Mode 1: graph data (safe, applied directly)
# --------------------------------------------------------------------------

def migrate_data(root: Path, *, backup: bool = True) -> int:
    out_dirs = _find_output_dirs(root)
    if not out_dirs:
        print("No graphify output directory found under", root)
        return 0

    touched = 0
    for d in out_dirs:
        for p in _iter_files(d):
            text = _read(p)
            if text is None:
                continue

            if p.suffix.lower() == ".json":
                try:
                    data = json.loads(text)
                except json.JSONDecodeError:
                    continue
                new_data, n = migrate_json_keys(data)
                if n:
                    _backup_and_write(
                        p, json.dumps(new_data, indent=2, ensure_ascii=False) + "\n",
                        backup=backup,
                    )
                    print(f"  {p}  {n} key(s) renamed")
                    touched += 1

            elif p.name in GENERATED_REPORT_NAMES:
                hits = remaining_hits(text)
                if hits:
                    _backup_and_write(p, swap_term(text), backup=backup)
                    print(f"  {p}  {len(hits)} mention(s) updated")
                    touched += 1

    if touched:
        print(f"\nDone. {touched} file(s) updated." + ("  Backups written as *.bak." if backup else ""))
    else:
        print("Nothing to do - already up to date.")
    return touched


# --------------------------------------------------------------------------
# Mode 2: the user's own files (preview first, always)
# --------------------------------------------------------------------------

def migrate_docs(root: Path, *, backup: bool = True) -> int:
    """Rewrite the user's own files. This edits prose the tool does not
    understand, so it ALWAYS previews and ALWAYS asks first.

    There is deliberately NO --yes/--force flag to skip the preview, and one
    must never be added. Someone's notes may contain the word for entirely
    unrelated and legitimate reasons -- a religious text being the obvious
    case -- and silently rewriting those would be far worse than the problem
    this tool was built to solve. The confirmation is the whole safety model.
    """
    out_dirs = {d.resolve() for d in _find_output_dirs(root)}
    proposals: list[tuple[Path, list[tuple[int, str, str]]]] = []

    for p in _iter_files(root):
        if any(str(p.resolve()).startswith(str(d)) for d in out_dirs):
            continue  # handled by migrate_data
        text = _read(p)
        if text is None or not remaining_hits(text):
            continue
        lines = []
        for i, line in enumerate(text.splitlines(), 1):
            if remaining_hits(line):
                lines.append((i, line.strip(), swap_term(line).strip()))
        if lines:
            proposals.append((p, lines))

    if not proposals:
        print("Nothing to do - no files reference the old terminology.")
        return 0

    total = sum(len(v) for _, v in proposals)
    print(f"DRY RUN - nothing has been written yet.")
    print(f"{total} change(s) across {len(proposals)} file(s):\n")
    for p, lines in proposals:
        for ln, before, after in lines[:20]:
            print(f"  {p}:{ln}")
            print(f"      - {before[:100]}")
            print(f"      + {after[:100]}")
        if len(lines) > 20:
            print(f"  ... and {len(lines) - 20} more in this file")
    print()

    try:
        answer = input(f"Apply these {total} change(s)? [y/N] ").strip().lower()
    except EOFError:
        answer = ""  # non-interactive: treated as "no", never as "yes"
    if answer not in {"y", "yes"}:
        print("Aborted. Nothing was written.")
        return 0

    for p, _ in proposals:
        text = _read(p)
        if text is not None:
            _backup_and_write(p, swap_term(text), backup=backup)
    print(f"Done. {len(proposals)} file(s) updated." + ("  Backups written as *.bak." if backup else ""))
    return len(proposals)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="halal-graphify migrate",
        description=(
            "Convert a project that still uses the upstream Graphify terminology. "
            "By default only machine-generated graph data is converted, which is "
            "always safe. Use --docs to also update your own files."
        ),
    )
    ap.add_argument("path", nargs="?", default=".", help="project directory (default: .)")
    ap.add_argument("--docs", action="store_true",
                    help="also update your own files, after showing a preview and asking")
    ap.add_argument("--no-backup", action="store_true", help="do not write .bak files")
    # NOTE: there is intentionally no --yes/--force. See migrate_docs().
    args = ap.parse_args(argv)

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2

    backup = not args.no_backup
    print(f"Migrating {root}\n")
    migrate_data(root, backup=backup)
    if args.docs:
        print()
        migrate_docs(root, backup=backup)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
