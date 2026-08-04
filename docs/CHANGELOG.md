# Changelog

## 2026-08-04 — Godot / GDScript support added as a regeneration-safe overlay

**Why.** Upstream Graphify has no GDScript backend at all: every `.gd` file lands in
`unclassified`, so a Godot project graphs to nothing useful. That is the measured reason
`EndlessShooter` forbids graphify entirely (see the global Rule 6 note). Omar wanted Godot work
covered without giving up the rename, so the support comes here rather than by switching to some
other fork.

**Not written from scratch — ported.** Three candidate Godot forks exist. The one taken is
`Epic-Millennium/graphify-godot` (branch `feat/gdscript-extractor`), itself a port of Bruno
Hidalgo's `hidalgob/graphify-godot` onto upstream v0.9.23. Rejected: `hidalgob/graphify-godot`
(based on 0.5.0, ~30 releases stale) and `Pero122/graphify-gdscript` (0.8.50, ships only a test
file). None of the three is a real GitHub fork — all are standalone copies, so there is no upstream
PR to track.

**Conflicts: none.** The port's whole diff against upstream 0.9.23 is one new extractor, one new
test file, and four surgical insertions. Every insertion anchor was checked against our 0.9.32 tree
and found present and unchanged, so it applied without modification.

**How it is wired — this is the part a future session must not undo.** The source tree here is
GENERATED (`rename.py` + `sync.py`), so the extractor is **not** hand-edited into
`halal_graphify/`. It lives in `overlay/gdscript.py` and is installed by
`sync.py:_install_gdscript_extractor()`, which runs after `rename.py`, exactly like the `migrate`
verb. Editing the copy inside the package instead of `overlay/` means the next sync silently erases
the change.

Every edit that function makes to upstream's files is an **anchored insert**, never a rewrite, for
the same reason `migrate` is intercepted rather than added to the dispatch table: the shape of those
tables is upstream's to change. If an anchor ever disappears the sync **stops loudly** rather than
publishing a half-wired release — a silently skipped patch would ship a build where `.gd` files are
detected but never dispatched. It patches: `detect.py` (CODE_EXTENSIONS), `extract.py` (import,
extension→language map, extension→extractor dispatch), `extractors/__init__.py` (registry),
`pyproject.toml` (the extra), `README.md` (two table rows), `NOTICE` (attribution). It is idempotent
— verified by running it twice and diffing.

**The grammar is an optional extra `[godot]`, not a core dependency.** GDScript has no standalone
`tree-sitter-gdscript` wheel on PyPI (checked: 404); the only source is `tree-sitter-language-pack`,
which bundles ~150 grammars and is large. Making it core would tax every install for a language most
users never touch. `.tscn`/`.tres` are pure regex and need nothing. Omar chose this over a core
dependency. The missing-grammar path returns a clear error naming the exact install command rather
than just reporting what is absent.

**Attribution.** `LICENSE` is untouched (Apache-2.0 §4 requires it verbatim); provenance goes in
`NOTICE`, plus a lineage block in the extractor's own header.

**The guard still passes with zero offences.** "Godot" contains the forbidden substring, and the
transform already treats it as a protected word — that was verified here, not assumed.

**Testing.** Full suite before: 64 failed / 3658 passed. After: 64 failed / **3661** passed — the
+3 are exactly the new GDScript tests, so zero regressions. (Those 64 pre-existing failures are
environmental — optional extras like `tree-sitter-hcl` are not installed locally — and are
unrelated to this work.) End-to-end on a real Godot project produced 12 nodes / 13 edges with
correct `aliases`, `contains`, `inherits`, `imports_from` (cross-file `preload`), `emits` and
`calls`.

Two of the three ported tests were marked `@requires_grammar`, and the module warms the parser at
import time. Reason: `tests/conftest.py` sandboxes `HOME`/`LOCALAPPDATA` to a throwaway directory,
and `tree_sitter_language_pack` resolves its grammar cache from exactly those variables, so inside a
test it fails with "Could not determine system cache directory" **and memoises that failure**.
Module import happens at collection, before the sandbox fixture applies, so warming there gets a
real cache directory. Without the skip marker the absolute-path-leak test would pass *vacuously* on
an empty graph — it was doing so before the marker was added.

### Releasing this out of band — `.postN`, and the tag must move

Two traps, both hit while shipping this and both easy to repeat:

1. **`halal-graphify 0.9.32` was already on PyPI**, and the publish step uses `skip-existing: true`,
   so republishing that version would have *silently done nothing*. A fork-local release that
   carries no new upstream code therefore takes a **PEP 440 post-release**: `0.9.32.post1`. Do not
   use `0.9.33` — upstream will want that number, and the two would then mean different things.
   Do not use `0.9.32+godot1` either: PyPI rejects local versions outright.
2. **The publish job checks out `needs.sync.outputs.tag`** — the tag named in `upstream-tag.txt` —
   **not `main`.** Committing to `main` without moving `v0.9.32` would have built and published the
   pre-Godot tree. The tag was force-moved onto the release commit.

The version bump lives in the generated `pyproject.toml` and is deliberately **not** carried in the
overlay: the next sync to a real upstream release resets the version to that release's number, which
is exactly what should happen.

### ⚠️ Known limitation — scene→script edge is lost when `X.gd` and `X.tscn` share a stem

Upstream's `_file_node_id()` is `{parent_dir}_{stem}` with the **extension dropped**, so Godot's
standard pairing of `player.gd` with `player.tscn` collapses both files onto one id. Upstream's
disambiguation then renames both, and the `.tscn` → `.gd` `imports_from` edge dangles and is pruned.

Confirmed by experiment: with non-colliding names (`main.tscn` → `player.gd`) the edge survives;
with the colliding pair it disappears. **Everything else is unaffected** — the `.gd` graph itself
(classes, functions, signals, `calls`, `inherits`, cross-file `preload`) is fully intact in both
cases; only that one cross-file edge is lost.

This is pre-existing in the upstream id scheme and is **not** introduced by this integration.
Deliberately NOT worked around: a correct fix belongs in upstream's id/disambiguation logic, and
faking an id in our extractor would either produce a dangling edge anyway or a duplicate one. Left
documented rather than hacked.

## 2026-08-04 — README names the old term openly; migrate documented

**The rule is about attribution, not the word itself.** Omar's ruling, and it governs every future
edit here: what must never happen is *calling something a god* — naming a node, a class or anything
else that way. Saying the word in order to report what was removed is a mention, not an attribution,
and is fine.

So the README banner now states plainly that what upstream calls "god nodes" are called "hub nodes"
here, instead of talking around it. That is also strictly better for the fork's purpose: someone
searching for exactly this problem can now find the repo.

What did **not** change: the generated code, the CLI, the reports and every other output still
contain zero occurrences. The rename is unchanged — only the fork's own explanatory banner names it.

`rename.py:guard()` blanks the exact `FORK_NOTICE` block before scanning `README.md`, rather than
skipping the file. A stray occurrence anywhere else in that README still fails the sync; verified by
injecting one and confirming the guard reports it.

Also added to the README, under **"Coming from the original Graphify?"**: the `migrate` command, both
modes, the `.bak` backups, the reason `--docs` can never be made non-interactive, the protected words,
`migrate.bat`, and the list of names deliberately left alone (`graphify-out/`, `GRAPHIFY_OUT`,
`.graphifyignore`, `.graphifyinclude`).

Internal docs restored to plain wording for the same reason — describing `gods` → `hubs` precisely is
more useful to a future maintainer than talking around it.

## 2026-08-04 — Fork created

Created `halal-graphify`, a fork of [Graphify](https://github.com/Graphify-Labs/graphify) that
removes the original's deity-based terminology for highly-connected nodes, replacing it with the
standard graph-theory term **hub node**. Built against upstream `v0.9.32`.

### Why "hub" and not "super"

"Hub node" is the actual term in graph theory for a high-degree vertex. Choosing it means the fork
reads as using the correct technical word rather than as censorship, which makes it far easier to
justify to someone who has not read this file. The concept, maths and output are unchanged.

### Design decisions that must not be re-litigated

**The tree is generated, never merged.** `rename.py` transforms a fresh upstream checkout; `sync.py`
replaces the fork's tree wholesale. There is no `git merge` anywhere, which is why a resync cannot
produce a conflict. Upstream ships very frequently (~200 releases), so a hand-edited fork would have
rotted within weeks. The price is that the fork does not carry upstream's commit history and cannot
send PRs back upstream. That was accepted deliberately.

**Track tags, not a branch.** Upstream's `main` is stale at `0.1.14` while releases are at `0.9.x`;
releases ship from versioned branches (`v1`…`v8`), and `refs/heads/v8` was identical to
`refs/tags/v0.9.32`. Tracking the newest semver tag lands on a real release and survives the roll to
`v9` with no edit. **Do not "fix" the sync to follow `main`.**

**The old term is quarantined in `overlay/migrate.py`, on purpose.** A tool that removes a word must
contain it to search for it. Obfuscating it (building the string from fragments at runtime to defeat
`grep`) was considered and rejected: it produces a clean `grep` and misleading code. The guard
excludes exactly two things — that file, and the licence texts, which must stay verbatim under
Apache-2.0 §4. The exclusions are listed literally rather than by pattern, so the exclusion list
cannot quietly become a hiding place.

**The guard fails closed.** If a future upstream release introduces a spelling the transform does not
cover, `rename.py` exits non-zero, `sync.py` publishes nothing, and the workflow opens an issue. That
is the intended behaviour, not a bug to work around.

**`migrate --docs` has no `--yes` flag, and must never get one.** It rewrites prose the tool does not
understand. Someone's notes may contain the word for entirely unrelated and legitimate reasons — a
religious text being the obvious case — and silently rewriting those would be worse than the problem
this fork exists to solve. The confirmation *is* the safety model. A non-interactive run reads EOF and
is treated as "no", never as "yes". (`overlay/migrate.py:migrate_docs`)

**Names in the user's project are not renamed.** `graphify-out`, `GRAPHIFY_OUT`, `.graphifyignore`,
`.graphifyinclude`, `.graphify` are parked in `rename.py:KEEP_LITERALS`. Keeping them means the fork
reads graphs and config people already have, and the two tools stay interoperable. Only the word
inside the output was ever the problem.

**JSON migration renames structural keys only, never values.** A user whose codebase contains a
function named with the old term would have their graph corrupted by a blind text replace. See
`JSON_KEY_MAP` in `overlay/migrate.py`.

### Findings from building it, worth keeping

**There IS a false positive.** An early survey of the installed package suggested none. At full repo
scale that was wrong: `tygodnie` (Polish for "weeks") appears in
`docs/translations/README.pl-PL.md` and contains the letters of the old term. A naive substring
replace mangles the Polish translation. Hence `PROTECTED_WORDS` in `overlay/migrate.py`, which also
defensively covers `godot`, `godzin`, `godina`, `pagoda`. **Do not remove that mechanism** — it is
load-bearing, and verified by the Polish file surviving each sync.

Translated docs DO carry translated compounds — Dutch `godknooppunten`, Uzbek `god-tugunlar`. Those
are genuine targets, and the transform catches them because it works on the substring rather than on
whole words.

**Hyphen vs underscore caused every real bug in the transform.** Recorded in `CLAUDE.md`. The
specific failures found by running upstream's test suite:

| Symptom | Cause | Fix |
|---|---|---|
| `No module named halal-graphify` | `python -m graphify` took the distribution name | rule 4b: `-m` takes the module name |
| `packages = ["halal-graphify"]` — wheel installs nothing | CLI-name heuristics leaked into TOML | `identity_literals=False` for pyproject |
| `missing artifact: halal-graphify/skill.md` | repo-relative path took the hyphen form | rule 4d: `graphify/` → `halal_graphify/` |
| `KeyError: 'halal-graphify'` | package-data key is a package name | rule 4e |
| stray old name in user-facing prose | lookahead `(?!\.)` also blocked end-of-sentence "graphify." | narrowed to real file extensions |
| `halal-halal-graphify` | hyphen is a word boundary, so rule 6 re-matched its own output | added lookbehind `(?<![-\w])` |

**Running upstream's test suite is the real verification, and it must stay in the sync.** It caught
every one of the above. A transform this broad cannot be trusted on inspection alone.

Test results against `v0.9.32`: **3698 passed**. Baseline (unmodified upstream, same environment)
had 64 failures from missing optional dependencies; the fork has those same 64 plus **5 documented
divergences** in `fork-divergences.txt` — a hyphen-hostile regex in a hook test, one deliberate
behavioural difference (we never delete the original tool's hooks, which is what coexistence
requires), and three `skillgen` tests bound to a pinned upstream commit SHA that a regenerated fork
cannot reach.

**Correction to an early assumption:** `hub-nodes` was expected to return an empty list on an
un-migrated graph. It does not — it recomputes from `graph.json`. The stale key only affects commands
that read the cached analysis sidecar (`report`, `explain`, `export wiki`, via `_an.get(...)`).
Migration still matters, but the failure mode is narrower than first described.

### Verified end to end

Original graphify generated a real graph; `halal-graphify migrate` converted its
`.graphify_analysis.json` (`gods` → `hubs`), left every value untouched, wrote `.bak` backups, and
reported "nothing to do" on a second run. `--docs` previewed changes, wrote nothing on EOF, applied
them on `y`, and left the Polish false-positive file alone in both cases.
