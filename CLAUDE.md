# halal-graphify

**Criticality tier:** `normal`

An unofficial fork of [Graphify](https://github.com/Graphify-Labs/graphify) that replaces the
original's deity-based name for highly-connected nodes with **"hub node"**. Public, Apache-2.0,
published to PyPI as `halal-graphify`.

It also carries capabilities upstream lacks, installed as overlays: **Godot / GDScript extraction**
(`.gd` AST plus `.tscn`/`.tres` scenes, ported from `graphify-godot`; `.gd` needs the optional
`[godot]` extra) and the **`view` verb** (architecture views computed from `graphify-out/graph.json`
with no LLM calls — map/area/file/node/impact/trace/flaws/stats). Secondary to the rename by design —
see the changelog rows before changing either.

## The one invariant

**The rule is about attribution, not the word.** Nothing may *call* a node — or anything else — a
god. That is the naming the fork exists to remove, and it must never appear in the code, the CLI, the
reports or any generated output. Saying the word to *explain what was removed* is a mention, not an
attribution, and is allowed. Omar's ruling; do not narrow or widen it.

`rename.py`'s guard enforces this and fails the whole sync rather than shipping a usage. Three places
legitimately contain the word:

| Where | Why |
|---|---|
| `migrate.py` (source in `overlay/`, copy in the package — same file) | a tool that removes a word must contain it to search for it |
| the `FORK_NOTICE` banner in `README.md` | states plainly what was renamed, so people can find the fork |
| `docs/CHANGELOG.md` | engineering record; describes the transform precisely |

The guard blanks the exact banner text before scanning `README.md`, so **any other** occurrence in
that file still fails. Do not relax that into skipping the file.

Two more things a bare `grep -ri` surfaces that are not the term at all:
`docs/translations/README.pl-PL.md` holds the Polish word for "weeks", and `docs/graph-hero.png` is a
binary image whose compressed bytes happen to contain that byte sequence.

## How this repo works — read this before changing anything

The source tree is **generated, not edited**. It is rebuilt from an upstream release tag by
`rename.py` on every sync, so:

- **Never hand-edit anything outside the fork-owned files below.** Your edit will be erased on the
  next sync. Change `rename.py` instead.
- There is no `git merge` in the pipeline, which is why a resync cannot conflict.

| Fork-owned (survives a sync) | What it is |
|---|---|
| `rename.py` | the transform + the guard |
| `overlay/migrate.py` | the `migrate` verb; sole home of the old term |
| `overlay/gdscript.py` | the Godot/GDScript extractor (upstream has none) |
| `overlay/test_gdscript.py` | its tests |
| `overlay/views.py` | the `view` verb: architecture views from graph.json, no LLM |
| `overlay/test_views.py` | its tests |
| `sync.py` | fetch newest upstream tag → rename → overlay → commit |
| `fork-divergences.txt` | upstream tests that cannot pass in a fork, each with a reason |
| `.github/workflows/sync.yml` | weekly sync + PyPI publish |
| `update.bat`, `migrate.bat` | double-click entry points |
| `CLAUDE.md`, `docs/CHANGELOG.md` | these |

Everything else is regenerated upstream code.

## Names that must NOT be renamed

These live in the *user's* project, so renaming them would break graphs and config people already
have: `graphify-out`, `GRAPHIFY_OUT`, `.graphifyignore`, `.graphifyinclude`, `.graphify`.
They are parked in `rename.py:KEEP_LITERALS`. Upstream URLs are parked too (attribution).

## Hyphen vs underscore — the trap that caused most bugs

| Form | Used for | Example |
|---|---|---|
| `halal-graphify` | distribution name, CLI command, skill folder, user-facing prose | `pip install halal-graphify` |
| `halal_graphify` | python package, `python -m`, repo paths, setuptools keys | `from halal_graphify.analyze import hub_nodes` |

Getting these backwards produces a wheel that installs nothing, or a CLI that cannot import itself.
`rename.py`'s rules 4a–6 exist entirely to keep them apart.

## Commands

```bash
python rename.py <checkout>     # transform a tree (used by sync)
python sync.py --check          # is there a newer upstream release?
python sync.py                  # regenerate, commit, tag
pytest tests -q                 # upstream's suite; see fork-divergences.txt
```

## Read on demand

| File | Answers | Cost |
|---|---|---|
| `docs/CHANGELOG.md` | why something is the way it is; what a past session decided | grows |
| `fork-divergences.txt` | why a given test is expected to fail | ~1k |
| `rename.py` docstrings | what each transform rule protects against | ~3k |

## Change log

| Date | Headline | Read before touching |
|---|---|---|
| 2026-08-04 | Fork created: transform, guard, migrate verb, weekly sync, PyPI publish | all of it — `docs/CHANGELOG.md` |
| 2026-08-04 | Godot/GDScript added as an overlay + `[godot]` extra; known `X.gd`/`X.tscn` id-collision caveat | `overlay/gdscript.py`, `sync.py:_install_gdscript_extractor` |
| 2026-08-25 | `view` verb (map/area/file/node/impact/trace/flaws/stats) + generalised fork-verb hook + regeneration-safe `.postN` versioning (`FORK_POST`) → 0.9.32.post2 | `overlay/views.py`, `sync.py:_register_fork_verbs`, `_set_fork_version` |
