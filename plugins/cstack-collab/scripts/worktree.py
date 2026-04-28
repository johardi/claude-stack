#!/usr/bin/env python3
"""Discover and inspect Claude agent worktrees.

A "Claude agent worktree" is a `git worktree` whose admin directory
(`.git/worktrees/<name>/`) carries the `locked` marker
``claude agent <id> (pid <N>)``. The Claude Code harness emits these for
``Agent({isolation: "worktree"})`` spawns. They are the worktrees that
``handoff`` / ``reclaim`` / ``list-worktrees`` operate on — never plain
user-created worktrees.

Subcommands:
    list [--json]
        List Claude agent worktrees with branch, lock state (live PID /
        stale / unlocked), dirty/clean, and unpushed-commit status.
        Default output is human-readable; ``--json`` returns a list of
        objects suitable for downstream scripting.

    inspect <ref> [--json]
        Same as ``list`` but for a single worktree. ``<ref>`` is either
        a branch name, an agent ID (the ``agent-<hash>`` slug), or an
        absolute path. Exits 1 if no match. Exits 2 if multiple match.

    repo-root
        Print the path to the *primary* repo root (the one that owns
        ``.git/worktrees/``). Useful for scripts that need to know
        where ``state.json`` lives regardless of cwd. Exits 1 if not
        inside a git repo.

Exit codes:
    0   success
    1   no match / not a git repo
    2   ambiguous match / usage error
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

LOCK_RE = re.compile(r"^claude agent (?P<agent>\S+)(?: \(pid (?P<pid>\d+)\))?")


@dataclass
class Worktree:
    path: str
    branch: str | None
    head: str
    agent_id: str | None
    lock_pid: int | None
    lock_alive: bool
    dirty: bool
    unpushed: int
    admin_dir: str

    def to_dict(self) -> dict:
        return asdict(self)


def _run(cmd: list[str], cwd: str | None = None) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True)


def _git_common_dir() -> Path:
    out = _run(["git", "rev-parse", "--git-common-dir"]).strip()
    return Path(out).resolve()


def repo_root() -> Path:
    """Return the primary repo root (the one whose .git/ is a real dir,
    not a worktree gitfile pointer)."""
    common = _git_common_dir()
    return common.parent.resolve()


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False
    except OSError:
        return False


def _parse_lock(lock_path: Path) -> tuple[str | None, int | None]:
    if not lock_path.is_file():
        return None, None
    text = lock_path.read_text().strip()
    m = LOCK_RE.match(text)
    if not m:
        return None, None
    pid = int(m.group("pid")) if m.group("pid") else None
    return m.group("agent"), pid


def _is_dirty(path: Path) -> bool:
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(path),
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        return False
    return bool(out.stdout.strip())


def _unpushed_count(path: Path, branch: str | None) -> int:
    if not branch:
        return 0
    try:
        out = subprocess.run(
            ["git", "rev-list", "--count", f"@{{u}}..HEAD"],
            cwd=str(path),
            text=True,
            capture_output=True,
        )
    except FileNotFoundError:
        return 0
    if out.returncode != 0:
        return 0
    try:
        return int(out.stdout.strip())
    except ValueError:
        return 0


def _list_worktree_porcelain() -> list[dict]:
    """Parse `git worktree list --porcelain` into a list of dicts."""
    out = _run(["git", "worktree", "list", "--porcelain"])
    entries: list[dict] = []
    cur: dict = {}
    for line in out.splitlines():
        if not line.strip():
            if cur:
                entries.append(cur)
                cur = {}
            continue
        key, _, value = line.partition(" ")
        cur[key] = value or True
    if cur:
        entries.append(cur)
    return entries


def discover() -> list[Worktree]:
    """Return only worktrees that look like Claude agent worktrees."""
    common = _git_common_dir()
    admin_root = common / "worktrees"
    results: list[Worktree] = []
    for entry in _list_worktree_porcelain():
        path = entry.get("worktree")
        if not path or path is True:
            continue
        admin_name = Path(path).name
        admin_dir = admin_root / admin_name
        agent_id, pid = _parse_lock(admin_dir / "locked")
        # Fallback: the harness drops a CLAUDE_BASE marker even when the
        # lock has been released or rewritten.
        if agent_id is None and not (admin_dir / "CLAUDE_BASE").is_file():
            continue
        if agent_id is None:
            agent_id = admin_name
        branch = entry.get("branch")
        if isinstance(branch, str) and branch.startswith("refs/heads/"):
            branch = branch[len("refs/heads/") :]
        elif branch is True:
            branch = None
        head = entry.get("HEAD", "") or ""
        lock_alive = bool(pid and _pid_alive(pid))
        results.append(
            Worktree(
                path=path,
                branch=branch,
                head=head if isinstance(head, str) else "",
                agent_id=agent_id,
                lock_pid=pid,
                lock_alive=lock_alive,
                dirty=_is_dirty(Path(path)),
                unpushed=_unpushed_count(Path(path), branch),
                admin_dir=str(admin_dir),
            )
        )
    return results


def _match(worktrees: list[Worktree], ref: str) -> list[Worktree]:
    abs_ref = str(Path(ref).resolve()) if not ref.startswith("refs/") else ref
    matches: list[Worktree] = []
    for w in worktrees:
        if w.branch == ref or w.agent_id == ref or w.path == abs_ref:
            matches.append(w)
    return matches


def _format_human(w: Worktree) -> str:
    if w.lock_pid is None:
        lock_state = "unlocked"
    elif w.lock_alive:
        lock_state = f"locked (pid {w.lock_pid} alive)"
    else:
        lock_state = f"locked (pid {w.lock_pid} dead — stale lock)"
    flags = []
    if w.dirty:
        flags.append("dirty")
    if w.unpushed:
        flags.append(f"{w.unpushed} unpushed")
    if not flags:
        flags.append("clean")
    branch = w.branch or "(detached)"
    return (
        f"{w.agent_id}\n"
        f"  path:   {w.path}\n"
        f"  branch: {branch}\n"
        f"  lock:   {lock_state}\n"
        f"  state:  {', '.join(flags)}\n"
    )


def cmd_list(args: argparse.Namespace) -> int:
    worktrees = discover()
    if args.json:
        print(json.dumps([w.to_dict() for w in worktrees], indent=2))
        return 0
    if not worktrees:
        print("No Claude agent worktrees found.")
        return 0
    for w in worktrees:
        print(_format_human(w))
    return 0


def cmd_inspect(args: argparse.Namespace) -> int:
    worktrees = discover()
    matches = _match(worktrees, args.ref)
    if not matches:
        print(f"error: no agent worktree matches {args.ref!r}", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(
            f"error: {len(matches)} worktrees match {args.ref!r} — "
            "disambiguate by agent id or absolute path",
            file=sys.stderr,
        )
        return 2
    w = matches[0]
    if args.json:
        print(json.dumps(w.to_dict(), indent=2))
    else:
        print(_format_human(w))
    return 0


def cmd_repo_root(args: argparse.Namespace) -> int:
    try:
        print(str(repo_root()))
    except subprocess.CalledProcessError:
        print("error: not inside a git repository", file=sys.stderr)
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("list", help="list Claude agent worktrees")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("inspect", help="inspect one Claude agent worktree")
    s.add_argument("ref", help="branch, agent id, or absolute path")
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_inspect)

    s = sub.add_parser(
        "repo-root", help="print the primary repo root (where state.json lives)"
    )
    s.set_defaults(func=cmd_repo_root)

    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
