"""Turn an upstream Graphify checkout into halal-graphify.

This is the heart of the fork. The fork's source tree is not hand-edited and
never merged -- it is GENERATED from an upstream release tag by this script,
every time. That is what makes a resync structurally incapable of producing a
merge conflict: there is no merge, only a regeneration.

Two properties this script must always have:

  * TOTAL      -- after it runs, the old term does not survive anywhere in the
                  generated tree (outside the quarantined module and the
                  licence files). Enforced by the guard at the end, which
                  fails the whole sync rather than shipping the word.
  * IDEMPOTENT -- running it twice produces a byte-identical tree.

Note that this file contains no literal of the old term. Its vocabulary is
imported from the one module allowed to hold it, overlay/migrate.py.

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
QUARANTINED = {f"{FORK_PKG}/migrate.py"}

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


# Deliberately worded so the banner itself does not contain the old term --
# otherwise this notice would be the one thing reintroducing it. The guard
# catches that mistake if anyone edits this string carelessly.
FORK_NOTICE = f"""> ### This is {FORK_DIST} — an unofficial fork of [Graphify](https://github.com/Graphify-Labs/graphify)
>
> **The only change: the original's deity-based name for its most-connected
> nodes is replaced with "hub node."** "Hub" is the standard graph-theory term
> for a highly connected vertex, so nothing is lost — the concept, the maths
> and the output are identical. Only the word changes.
>
> Made for Muslims, and for anyone else who would rather not have that word in
> their tools. Everything else is upstream, tracked automatically and released
> in step with it.
>
> Coming from the original? Run `{FORK_DIST} migrate .` once and your existing
> graphs keep working — no re-extract needed.
>
> Not affiliated with or endorsed by Graphify Labs.
> Licensed under Apache-2.0. This is a modified version of the original work.

"""


# --- the guard ------------------------------------------------------------

def guard(root: Path) -> list[str]:
    """Fail closed. Every surviving occurrence is reported as file:line."""
    offences: list[str] = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or any(d in SKIP_DIRS for d in p.parts):
            continue
        rel = p.relative_to(root).as_posix()
        if p.name in LICENCE_FILES or rel in QUARANTINED:
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
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
