"""Regenerate halal-graphify from the newest upstream release.

There is no `git merge` anywhere in this file, and that is the whole design.
The fork's tree is thrown away and rebuilt from an upstream tag on every sync,
so a resync cannot produce a merge conflict -- there is nothing to conflict
with. The cost is that the fork does not carry upstream's commit history; the
benefit is that this never needs a human to resolve anything.

Why tags and not a branch: upstream's `main` is stale (it sits at 0.1.14 while
releases are at 0.9.x). Releases ship from versioned branches -- v1 ... v8 --
and `refs/heads/v8` is currently identical to `refs/tags/v0.9.32`. Tracking the
newest semver TAG lands on a real release and survives the eventual roll to v9
without anyone editing this script.

Usage:
    python sync.py            # sync to newest upstream tag if there is one
    python sync.py --check    # report only, change nothing (exit 0 always)
    python sync.py --tag vX   # pin to a specific upstream tag
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
UPSTREAM = "https://github.com/Graphify-Labs/graphify"

# Files and directories that belong to the fork and must survive a regeneration.
# Everything else in the repo is generated and is replaced wholesale.
FORK_OWNED = {
    ".git", ".github", "rename.py", "sync.py", "overlay",
    "update.bat", "migrate.bat", "fork-divergences.txt",
    "CLAUDE.md", "docs/CHANGELOG.md", ".gitignore",
}

FORK_PKG = "halal_graphify"


def run(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    proc = subprocess.run(args, cwd=cwd, check=False,
                          capture_output=True, text=True, encoding="utf-8")
    if check and proc.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(args)}\n{proc.stderr}")
    return proc.stdout.strip()


def _semver(tag: str) -> tuple[int, ...] | None:
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", tag)
    return tuple(int(g) for g in m.groups()) if m else None


def newest_upstream_tag() -> str:
    """Highest semver tag upstream. Peeled refs (`^{}`) are skipped so a tag is
    not counted twice."""
    out = run("git", "ls-remote", "--tags", UPSTREAM)
    tags: list[tuple[tuple[int, ...], str]] = []
    for line in out.splitlines():
        if "\t" not in line or line.endswith("^{}"):
            continue
        name = line.split("refs/tags/", 1)[-1]
        ver = _semver(name)
        if ver:
            tags.append((ver, name))
    if not tags:
        raise SystemExit("no semver tags found upstream")
    return max(tags)[1]


def current_fork_tag() -> str | None:
    out = run("git", "tag", "--list", cwd=HERE, check=False)
    tags = [(v, t) for t in out.splitlines() if (v := _semver(t.strip()))]
    return max(tags)[1] if tags else None


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

    # Apply the overlay: fork-only files that must NOT go through rename.py.
    print("  applying overlay ...")
    shutil.copy2(HERE / "overlay" / "migrate.py", src / FORK_PKG / "migrate.py")
    _register_migrate_verb(src / FORK_PKG / "__main__.py")
    return src


def _register_migrate_verb(main_py: Path) -> None:
    """Wire `halal-graphify migrate` into the CLI dispatcher.

    Done by injection rather than by patching upstream's dispatch table,
    because that table's shape is upstream's to change. Intercepting before
    dispatch is stable across upstream refactors.
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
    pattern = re.compile(r"(?m)^(def main\([^)]*\)[^:]*:\n)((?:[ \t]+(?:\"\"\".*?\"\"\"|'''.*?''')\n)?)",
                         re.DOTALL)
    m = pattern.search(text)
    if not m:
        raise SystemExit("could not find `def main(` in __main__.py to wire `migrate` into")

    # Call goes after main()'s docstring, so the docstring stays a docstring.
    text = text[:m.start()] + hook + m.group(1) + m.group(2) + "    _hg_migrate_hook()\n" + text[m.end():]
    main_py.write_text(text, encoding="utf-8")


def swap_tree(generated: Path) -> None:
    """Replace the fork's generated content with the new tree, preserving the
    files the fork owns."""
    for entry in HERE.iterdir():
        rel = entry.name
        if rel in FORK_OWNED:
            continue
        if entry.is_dir():
            shutil.rmtree(entry, ignore_errors=True)
        else:
            entry.unlink()

    for entry in generated.iterdir():
        dst = HERE / entry.name
        if entry.name in FORK_OWNED:
            continue
        if entry.is_dir():
            shutil.copytree(entry, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(entry, dst)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report whether a newer release exists; change nothing")
    ap.add_argument("--tag", help="pin to a specific upstream tag")
    ap.add_argument("--no-commit", action="store_true", help="leave changes unstaged")
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

    if args.no_commit:
        print(f"\nDone (uncommitted). Review, then tag as {target}.")
        return 0

    run("git", "add", "-A", cwd=HERE)
    status = run("git", "status", "--porcelain", cwd=HERE, check=False)
    if not status:
        print("Tree identical to what is already committed. Nothing to do.")
        return 0

    run("git", "commit", "-q", "-m",
        f"sync: upstream {target} -> halal-graphify {target.lstrip('v')}", cwd=HERE)
    run("git", "tag", "-f", target, cwd=HERE)
    print(f"\nCommitted and tagged {target}. Push with:  git push --follow-tags")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
