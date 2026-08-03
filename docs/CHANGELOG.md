# Changelog

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

Translated docs DO carry translated compounds of the term — the Dutch, Uzbek and several other
`docs/translations/README.*.md` files splice it onto a local word for "node". Those are genuine
targets, and the transform catches them because it works on the substring rather than on whole words.

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
`.graphify_analysis.json` (stale analysis key → `hubs`), left every value untouched, wrote backups, and
reported "nothing to do" on a second run. `--docs` previewed changes, wrote nothing on EOF, applied
them on `y`, and left the Polish false-positive file alone in both cases.
