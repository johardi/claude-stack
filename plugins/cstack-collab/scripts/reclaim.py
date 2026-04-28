#!/usr/bin/env python3
"""Reclaim a Claude agent worktree from the primary repo (rescue mode).

Used when an agent is dead, abandoned, or the user wants the branch back
without the live agent's cooperation. Run from anywhere inside the
primary checkout (NOT from inside an agent worktree).

Steps it performs, in order:

    1. Locate the worktree by ``<ref>`` (branch name, agent id, or
       absolute path). Refuse if no match or multiple match.
    2. If the lock points at a *live* PID, refuse without ``--force`` —
       removing under a live agent kills the session mid-thought.
    3. If the worktree is dirty: unless ``--discard``, stash the dirty
       state to a recovery ref ``cstack-collab/reclaim/<agent-id>`` so
       the work isn't lost. The stash points to a real commit, so it
       survives ``git worktree remove`` and the user can recover via
       ``git stash apply <ref>`` or ``git cherry-pick <ref>``.
    4. ``git worktree unlock`` then ``git worktree remove`` (with
       ``--force`` for unpushed commits / locked-by-stale-pid cases).
    5. If ``--checkout`` was passed, switch the primary repo to the
       reclaimed branch in one shot.
    6. If a cstack-collab orchestration is active, append a
       ``reclaimed`` event to ``state.json`` so the audit trail isn't
       broken.

Exit codes:
    0   success
    1   no match / not in a git repo
    2   refused (live agent without --force, dirty without --stash/--discard,
        usage error)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import worktree as wt


def _run(cmd: list[str], cwd: Path | str | None = None, check: bool = True) -> str:
    out = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )
    if check and out.returncode != 0:
        sys.stderr.write(out.stderr)
        raise SystemExit(out.returncode or 1)
    return out.stdout


def _stash_to_ref(w: wt.Worktree, ref_name: str) -> str | None:
    """Create a stash from the worktree's dirty state and copy it to a
    durable ref. Returns the ref if anything was stashed, None otherwise.
    """
    if not w.dirty:
        return None
    # `git stash create` produces a stash commit object without touching
    # the stash list — perfect for moving to a named ref.
    sha = _run(
        ["git", "stash", "create", f"cstack-collab reclaim {w.agent_id}"],
        cwd=w.path,
    ).strip()
    if not sha:
        return None
    full_ref = f"refs/{ref_name}"
    _run(
        ["git", "update-ref", full_ref, sha],
        cwd=w.path,
    )
    # Discard the dirty state in the worktree so `git worktree remove`
    # doesn't refuse it. The work is preserved at `full_ref`.
    _run(["git", "reset", "--hard", "HEAD"], cwd=w.path)
    _run(["git", "clean", "-fd"], cwd=w.path)
    return full_ref


def _append_event(state_path: Path, event: dict) -> None:
    data = json.loads(state_path.read_text())
    data.setdefault("events", []).append(event)
    state_path.write_text(json.dumps(data, indent=2) + "\n")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("ref", help="branch name, agent id, or absolute path")
    p.add_argument(
        "--force",
        action="store_true",
        help="remove even when the agent's PID is still alive",
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument(
        "--stash",
        action="store_true",
        help="(default) preserve dirty state to refs/cstack-collab/reclaim/<id>",
    )
    g.add_argument(
        "--discard",
        action="store_true",
        help="throw away the dirty state in the worktree",
    )
    p.add_argument(
        "--checkout",
        action="store_true",
        help="after removing the worktree, check out the branch in the primary repo",
    )
    args = p.parse_args(argv)

    try:
        worktrees = wt.discover()
    except subprocess.CalledProcessError:
        print("error: not inside a git repository", file=sys.stderr)
        return 1

    matches = wt._match(worktrees, args.ref)
    if not matches:
        print(f"error: no agent worktree matches {args.ref!r}", file=sys.stderr)
        return 1
    if len(matches) > 1:
        print(
            f"error: {len(matches)} agent worktrees match {args.ref!r} — "
            "disambiguate by agent id or absolute path",
            file=sys.stderr,
        )
        return 2
    w = matches[0]

    if w.lock_alive and not args.force:
        print(
            f"refusing to reclaim {w.agent_id}: pid {w.lock_pid} is still "
            "alive (a live agent is using this worktree). Either ask the "
            "agent to run /cstack-collab:handoff, or pass --force to "
            "remove it anyway (the agent's session will fail).",
            file=sys.stderr,
        )
        return 2

    if w.dirty and not args.discard:
        # Default behavior: stash. --stash is for clarity, not required.
        ref_name = f"cstack-collab/reclaim/{w.agent_id}"
        stash_ref = _stash_to_ref(w, ref_name)
        if stash_ref:
            print(f"preserved dirty state at {stash_ref}")
            print(
                "  recover with: "
                f"git stash apply {stash_ref}   "
                f"(or: git cherry-pick {stash_ref})"
            )

    primary = wt.repo_root()

    # Unlock first — `git worktree remove` otherwise refuses a locked tree.
    _run(["git", "worktree", "unlock", w.path], cwd=primary, check=False)

    rm_cmd = ["git", "worktree", "remove", w.path]
    if args.force or w.unpushed:
        rm_cmd.append("--force")
    _run(rm_cmd, cwd=primary)
    print(f"removed worktree {w.path}")

    if args.checkout and w.branch:
        _run(["git", "checkout", w.branch], cwd=primary)
        print(f"checked out {w.branch} in {primary}")

    state_file_out = subprocess.run(
        [str(Path(__file__).with_name("state.py")), "find"],
        text=True,
        capture_output=True,
        cwd=str(primary),
    )
    state_path_str = state_file_out.stdout.strip()
    if state_file_out.returncode == 0 and state_path_str:
        _append_event(
            Path(state_path_str),
            {
                "event": "reclaimed",
                "agent_id": w.agent_id,
                "branch": w.branch,
                "at": datetime.now(timezone.utc).isoformat(),
                "forced": bool(args.force),
                "discarded": bool(args.discard),
            },
        )

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
