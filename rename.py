"""Turn an upstream Graphify checkout into halal-graphify.

This is the heart of the fork. The fork's source tree is not hand-edited and
never merged -- it is GENERATED from an upstream release tag by this script,
every time. That is what makes a resync structurally incapable of producing a
merge conflict: there is no merge, only a regeneration.

Two properties this script must always have:

  * TOTAL      -- after it runs, nothing in the generated tree NAMES anything a
                  god. Enforced by the guard at the end, which fails the whole
                  sync rather than shipping such a usage.
  * IDEMPOTENT -- running it twice produces a byte-identical tree.

The rule being enforced is about attribution, not the word itself: calling a
node a god is what must go. Saying the word to explain what was removed is a
mention, and is fine -- which is why FORK_NOTICE below states the change
plainly, and why the guard blanks exactly that banner (and nothing else)
before scanning README.md.

The transform's vocabulary is imported from overlay/migrate.py rather than
duplicated here, so the two can never drift apart.

Usage:  python rename.py <checkout-dir>
"""

from __future__ import annotations

import importlib.util
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# --- identity -------------------------------------------------------------

UPSTREAM_DIST = "graphifyy"          # upstream's name on PyPI
UPSTREAM_PKG = "graphify"            # upstream's python package directory
FORK_DIST = "halal-graphify"         # our name on PyPI, and our CLI command
FORK_PKG = "halal_graphify"          # our python package directory
FORK_REPO = "omar1001/halal-graphify"

# Names that live in the USER's project, not in ours. Deliberately NOT renamed:
# keeping them identical to upstream means halal-graphify reads the graphs and
# config you already have, and the two tools stay interoperable. None of these
# were ever the problem -- one word inside the output was.
#
# Longest first: _park() substitutes in order, so `.graphifyignore` must be
# claimed before the `.graphify` prefix can take a bite out of it.
KEEP_LITERALS = (
    ".graphifyignore",
    ".graphifyinclude",
    ".graphify",
    "graphify-out",
    "GRAPHIFY_OUT",
)

# Text files we transform. Anything else (images, wheels, lockfiles) is copied
# through untouched.
TEXT_SUFFIXES = {
    ".py", ".md", ".txt", ".json", ".toml", ".yml", ".yaml",
    ".html", ".svg", ".cfg", ".ini", ".sh", ".bat", ".ps1",
}

# Never modified: licence texts must stay verbatim (Apache-2.0 §4), and the
# quarantined module must keep the term it exists to search for.
LICENCE_FILES = {"LICENSE", "LICENSE-MIT", "NOTICE"}
# Both paths are the same file: the fork-owned source, and the copy the overlay
# places inside the package. During a sync the guard only ever sees the second,
# but listing both means running the guard over the repo root is also clean.
QUARANTINED = {f"{FORK_PKG}/migrate.py", "overlay/migrate.py"}

# Fork-authored files that may name the old term because they are *explaining
# what was removed* -- a mention, not an attribution -- or, in this script's
# case, because they hold the banner text that does the explaining.
#
# None of these ever reach a generated tree: they are fork-owned and restored
# after the transform, so during a real sync the guard never sees them. They
# are listed so that running the guard over the repo root is clean too.
FORK_AUTHORED = {"CLAUDE.md", "docs/CHANGELOG.md", "rename.py"}

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
             "dist", "build", ".venv", "venv", "node_modules", ".github"}


# --- vocabulary, imported from the single quarantined module ---------------

def _load_vocabulary():
    """Import overlay/migrate.py by path so this file never has to spell the
    old term itself. One definition, one place, no drift."""
    src = HERE / "overlay" / "migrate.py"
    spec = importlib.util.spec_from_file_location("_hg_vocab", src)
    if spec is None or spec.loader is None:
        raise SystemExit(f"cannot load vocabulary from {src}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


VOCAB = _load_vocabulary()
swap_term = VOCAB.swap_term
remaining_hits = VOCAB.remaining_hits


# --- package / identity rewriting -----------------------------------------

def discover_modules(pkg_dir: Path) -> set[str]:
    """The real module names inside the package, derived from the checkout
    rather than hardcoded -- so a module upstream adds next month is handled
    without touching this script.

    This allowlist is what makes the import rewrite safe. Upstream's tests
    reference literal filenames like `graphify.md` and `graphify.js`; because
    `md` and `js` are not modules, they are left alone automatically.
    """
    names = {p.stem for p in pkg_dir.glob("*.py")}
    names |= {p.name for p in pkg_dir.iterdir() if p.is_dir() and not p.name.startswith("__")}
    # Package-level attributes are accessed the same way (`graphify.__file__`)
    # and must follow the rename, or `import halal_graphify` leaves a dangling
    # `graphify.__file__` behind. Upstream's own tests catch this if it regresses.
    names |= {"__file__", "__path__", "__name__", "__doc__", "__version__", "__spec__"}
    return names


# Upstream's own web presence. These point at property we do not own, so
# renaming them would produce dead or misleading links -- and upstream's repo
# URL is read by the sync itself. Attribution depends on these staying exact.
UPSTREAM_URLS = (
    "github.com/Graphify-Labs/graphify",
    "Graphify-Labs/graphify",
    "safishamsi/graphify",
    "safi/graphify",
    "graphify.com",          # upstream's commercial site (Penpax)
)


def _park(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Park literals that must survive verbatim on placeholders no rewrite can
    match: names that live in the user's project, and upstream's own URLs."""
    guards: list[tuple[str, str]] = []
    literals = [*KEEP_LITERALS, *UPSTREAM_URLS]
    for i, lit in enumerate(literals):
        token = f"\x00K{i}\x00"
        guards.append((token, lit))
        text = text.replace(lit, token)
    return text, guards


def _unpark(text: str, guards: list[tuple[str, str]]) -> str:
    for token, lit in guards:
        text = text.replace(token, lit)
    return text


def rewrite_modules(text: str, modules: set[str], *, identity_literals: bool = True) -> str:
    """Package/distribution renames. Safe for every file type.

    `identity_literals` is switched off for pyproject.toml, where a bare
    "graphify" is a setuptools package name (underscore form) rather than a
    runtime identity string (hyphen form). Getting that backwards produces a
    wheel that installs nothing.
    """
    text, guards = _park(text)

    # 1. Module paths: only `graphify.<known-module>`. This allowlist is what
    #    keeps `graphify.md` and `graphify.js` (filenames in the test suite)
    #    from being mangled -- `md` and `js` are not modules.
    if modules:
        mods = "|".join(sorted((re.escape(m) for m in modules), key=len, reverse=True))
        text = re.sub(rf"\b{UPSTREAM_PKG}\.({mods})\b", rf"{FORK_PKG}.\1", text)

    # 2. Import statements.
    text = re.sub(rf"\bfrom {UPSTREAM_PKG}\b", f"from {FORK_PKG}", text)
    text = re.sub(rf"\bimport {UPSTREAM_PKG}\b", f"import {FORK_PKG}", text)

    # 3. The distribution name on PyPI.
    text = re.sub(rf"\b{UPSTREAM_DIST}\b", FORK_DIST, text)

    # 4. Path literals pointing at the package DIRECTORY inside the repo, e.g.
    #    `REPO_ROOT / "graphify"`. These take the underscore package name, not
    #    the hyphenated distribution name. Must run before rule 5, which would
    #    otherwise claim them.
    text = re.sub(rf'\b(REPO|REPO_ROOT|ROOT|repo|repo_root|root) / "{UPSTREAM_PKG}"',
                  rf'\1 / "{FORK_PKG}"', text)

    # 4b. `python -m graphify` takes the MODULE name (underscore), never the
    #     distribution name (hyphen) -- `python -m halal-graphify` fails with
    #     "No module named". Must run before rule 5, which would otherwise
    #     rewrite the quoted literal to the hyphen form.
    text = re.sub(rf'(["\']-m["\'],\s*["\']){UPSTREAM_PKG}(["\'])', rf"\1{FORK_PKG}\2", text)
    text = re.sub(rf"-m {UPSTREAM_PKG}\b", f"-m {FORK_PKG}", text)

    # 4c. Skill DESTINATION folders take the hyphen form (they sit next to
    #     other tools' skills, so they carry the tool's public name). Done
    #     before 4d so `skills/graphify/` is claimed first.
    text = text.replace(f"skills/{UPSTREAM_PKG}/", f"skills/{FORK_DIST}/")
    text = re.sub(rf'("skills"|"\.[a-z]+") / "{UPSTREAM_PKG}"', rf'\1 / "{FORK_DIST}"', text)

    # 4d. A repo-relative path INTO the package directory takes the underscore
    #     form: `graphify/skill.md` is a directory on disk, not a command name.
    text = re.sub(rf"\b{UPSTREAM_PKG}/", f"{FORK_PKG}/", text)

    # 4e. The [tool.setuptools.package-data] key is the package NAME, and tests
    #     look it up by that exact string.
    text = text.replace(f'["package-data"]["{UPSTREAM_PKG}"]',
                        f'["package-data"]["{FORK_PKG}"]')

    # 5. Every remaining bare `"graphify"` literal is a runtime IDENTITY string:
    #    the CLI binary looked up with shutil.which(), the MCP server name, the
    #    skill destination folder, and the substring used to recognise its own
    #    hooks. That last one matters for coexistence -- keyed on the fork's
    #    name, halal-graphify manages only its own hooks and leaves the
    #    original's alone. Quoted-with-suffix literals ("graphify.md",
    #    "graphify.js") do not match this pattern and are left alone.
    if identity_literals:
        text = re.sub(rf'(["\']){UPSTREAM_PKG}\1', rf"\1{FORK_DIST}\1", text)
        text = re.sub(rf'(["\']){UPSTREAM_PKG}\.exe\1', rf"\1{FORK_DIST}.exe\1", text)

        # 6. Every remaining standalone mention is the tool's own name in prose
        #    or in a user-facing message ("Usage: graphify <command>", "run
        #    'graphify install'", the --version banner). By this point the
        #    parked literals, module paths and imports have all been handled,
        #    so what is left is the CLI's identity.
        #
        #    The lookahead protects `graphify.md` / `graphify.js`, which are
        #    literal filenames in upstream's test fixtures, not references to
        #    the tool. It lists real extensions rather than "any dot", because
        #    a bare `(?!\.)` also blocks the very common end-of-sentence case
        #    ("...is not a reason to skip graphify.") and silently leaves the
        #    old name behind in user-facing prose.
        #
        #    The lookbehind stops this rule re-matching the output of the rules
        #    above -- without it, `halal-graphify` (hyphen is a word boundary)
        #    would grow another prefix on every pass.
        text = re.sub(
            rf"(?<![-\w]){UPSTREAM_PKG}\b(?!-)(?!\.(?:md|js|json|txt|py|html|svg|toml)\b)",
            FORK_DIST, text,
        )

    return _unpark(text, guards)


def rewrite_cli_name(text: str, *, prose: bool) -> str:
    """Rename the CLI command where it is used AS a command.

    Deliberately NOT applied to pyproject.toml: `graphify = [...]` is a TOML
    key, and the prose rules below would happily turn it into the invalid
    `halal-graphify = [...]`. Every rule here is scoped to a context that only
    occurs in documentation or in argv lists.
    """
    text, guards = _park(text)

    # argv lists in tests: ["graphify", "diagnose", ...]
    text = re.sub(rf'(["\']){UPSTREAM_PKG}\1(\s*,)', rf"\1{FORK_DIST}\1\2", text)
    text = re.sub(rf"\b{UPSTREAM_PKG}-mcp\b", f"{FORK_DIST}-mcp", text)

    if prose:
        # Shell examples: a line that starts with the command followed by a
        # subcommand. Requires a following word to avoid matching TOML keys.
        text = re.sub(rf"(?m)^(\s*(?:\$ )?){UPSTREAM_PKG}(?= +[a-z])", rf"\1{FORK_DIST}", text)
        text = re.sub(rf"`{UPSTREAM_PKG} (?=[a-z])", f"`{FORK_DIST} ", text)
        text = re.sub(rf"\b(uvx|pipx run|uv tool install|pip install) {UPSTREAM_PKG}\b",
                      rf"\1 {FORK_DIST}", text)

    return _unpark(text, guards)


def rewrite_pyproject(text: str, modules: set[str]) -> str:
    """pyproject gets module rules plus explicit, literal packaging fixes --
    no heuristics, because a wrong guess here produces a broken wheel."""
    text = rewrite_modules(text, modules, identity_literals=False)

    # setuptools package list: the bare "graphify" entry takes the UNDERSCORE
    # package name. Done before anything else could claim the literal.
    text = text.replace(f'packages = ["{UPSTREAM_PKG}"', f'packages = ["{FORK_PKG}"')

    # Console scripts. Upstream: graphify = "graphify.__main__:main"
    text = re.sub(rf'(?m)^{UPSTREAM_PKG} = "{FORK_PKG}\.', f'{FORK_DIST} = "{FORK_PKG}.', text)
    text = re.sub(rf'(?m)^{UPSTREAM_PKG}-mcp = "{FORK_PKG}\.', f'{FORK_DIST}-mcp = "{FORK_PKG}.', text)

    # [tool.setuptools.package-data] key, which is the package NAME, so it must
    # use the underscore form, not the distribution's hyphen form.
    text = re.sub(rf"(?m)^{UPSTREAM_PKG} = \[", f"{FORK_PKG} = [", text)

    # Point project URLs at the fork.
    text = re.sub(r'(Homepage|Repository) = "https://github\.com/Graphify-Labs/graphify"',
                  rf'\1 = "https://github.com/{FORK_REPO}"', text)
    text = text.replace('Issues = "https://github.com/Graphify-Labs/graphify/issues"',
                        f'Issues = "https://github.com/{FORK_REPO}/issues"')
    return text


# The banner names the old term openly. That is deliberate and was Omar's
# explicit call: the objection is to *calling something a god*, not to saying
# the word while explaining what was removed. Describing the change is a
# mention, not an attribution -- and naming it plainly is what lets people
# searching for exactly this actually find the fork.
#
# The guard strips this exact block before scanning README.md, so any OTHER
# occurrence in that file still fails the build.
FORK_NOTICE = f"""> ### This is {FORK_DIST} — an unofficial fork of [Graphify](https://github.com/Graphify-Labs/graphify)
>
> **The only change: what the original calls "god nodes" are called "hub nodes"
> here.** Nothing else differs — same analysis, same maths, same output, same
> commands. "Hub" is the standard graph-theory term for a highly connected
> vertex, so the name is arguably the more correct one anyway.
>
> Made for Muslims, and for anyone else who would rather their tools did not
> describe a piece of code that way. Everything else is upstream, tracked
> automatically and released in step with it.
>
> Not affiliated with or endorsed by Graphify Labs.
> Licensed under Apache-2.0. This is a modified version of the original work.

## Coming from the original Graphify?

**Your existing graphs keep working — you do not need to re-extract anything.**
Run this once inside a project you had already graphed:

```bash
{FORK_DIST} migrate .
```

That rewrites the stale key inside `graphify-out/` so the reports read
correctly. It is offline, uses no AI and costs nothing, writes a `.bak` backup
beside every file it touches, and is safe to run twice — the second run just
says there is nothing to do.

If your own notes, READMEs or agent rules also mention the old wording, add
`--docs`:

```bash
{FORK_DIST} migrate . --docs
```

That one **shows you every proposed change first and writes nothing until you
type `y`.** There is deliberately no flag to skip that confirmation: the tool
cannot tell your prose apart from a document that uses the word for entirely
unrelated and legitimate reasons, so you get the final say. Words that merely
contain the same letters — the Polish *tygodnie*, "Godot", "pagoda" — are
recognised and never touched.

On Windows you can also just double-click `migrate.bat` inside the project.

**What is *not* renamed, on purpose:** `graphify-out/`, `GRAPHIFY_OUT`,
`.graphifyignore` and `.graphifyinclude`. Those live in *your* project, so
leaving them alone means both tools read the same data and nothing you already
set up breaks.

"""


# --- the guard ------------------------------------------------------------

def guard(root: Path) -> list[str]:
    """Fail closed. Every surviving occurrence is reported as file:line."""
    offences: list[str] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(d in SKIP_DIRS for d in p.parts):
            continue
        rel = p.relative_to(root).as_posix()
        if p.name in LICENCE_FILES or rel in QUARANTINED or rel in FORK_AUTHORED:
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        # The fork's own banner names the old term on purpose (see FORK_NOTICE).
        # Blank out that exact block rather than skipping README.md wholesale,
        # so anything else in the file is still checked. Line numbers are kept
        # by substituting blank lines of the same count.
        if rel == "README.md" and FORK_NOTICE in text:
            text = text.replace(FORK_NOTICE, "\n" * FORK_NOTICE.count("\n"))

        for i, line in enumerate(text.splitlines(), 1):
            if remaining_hits(line):
                offences.append(f"{rel}:{i}: {line.strip()[:120]}")
    return offences


# --- driver ---------------------------------------------------------------

def transform(root: Path) -> None:
    pkg_dir = root / UPSTREAM_PKG
    if not pkg_dir.is_dir():
        raise SystemExit(f"no {UPSTREAM_PKG}/ package found in {root}")
    modules = discover_modules(pkg_dir)
    print(f"  discovered {len(modules)} modules for the import allowlist")

    changed = 0
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(d in SKIP_DIRS for d in p.parts):
            continue
        if p.name in LICENCE_FILES or p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            original = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        text = swap_term(original)
        if p.name == "pyproject.toml":
            text = rewrite_pyproject(text, modules)
        else:
            text = rewrite_modules(text, modules)
            text = rewrite_cli_name(text, prose=p.suffix.lower() in {".md", ".txt", ".html"})

        if p.name == "README.md" and p.parent == root and not text.startswith("> ###"):
            text = FORK_NOTICE + text

        if text != original:
            p.write_text(text, encoding="utf-8")
            changed += 1

    print(f"  rewrote {changed} files")

    # Rename the package directory last, so path-based logic above is stable.
    target = root / FORK_PKG
    if pkg_dir.exists():
        if target.exists():
            shutil.rmtree(target)
        pkg_dir.rename(target)
        print(f"  {UPSTREAM_PKG}/ -> {FORK_PKG}/")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    print(f"Transforming {root}")
    transform(root)

    print("  running guard...")
    offences = guard(root)
    if offences:
        print(f"\nGUARD FAILED - {len(offences)} occurrence(s) survived.\n", file=sys.stderr)
        for line in offences[:60]:
            print(f"  {line}", file=sys.stderr)
        if len(offences) > 60:
            print(f"  ... and {len(offences) - 60} more", file=sys.stderr)
        print(
            "\nUpstream has introduced a spelling this script does not cover.\n"
            "Add it to PROTECTED_WORDS (if it is unrelated) or extend the\n"
            "transform in overlay/migrate.py. Nothing has been published.",
            file=sys.stderr,
        )
        return 1

    print("  guard passed: zero occurrences outside the quarantined module.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
