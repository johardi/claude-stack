#!/usr/bin/env python3
"""Hand off this agent's worktree to the human (run from inside the agent).

Invoked when the human wants to take over the branch the live agent is
working on. The agent runs this script as the "I'm yielding" ritual:

    1. Verify we're inside a Claude agent worktree (otherwise refuse —
       this script is not meant for the primary repo).
    2. Inspect the worktree's state. If dirty:
         --commit "<msg>"   commit the dirty state on the current branch
         --stash            move dirty state to refs/cstack-collab/handoff/<id>
         --discard          throw it away
       If none of those is given AND the tree is dirty, refuse and list
       the changes so the agent (or human) picks an explicit action.
    3. If ``--push`` (default true), push the branch to ``origin`` so
       the human can fetch without needing the worktree.
    4. If a cstack-collab orchestration is active, append a
       ``handoff`` event to state.json with branch + last commit SHA +
       a short summary (``--summary "..."``).
    5. Print clear next-steps for the human (reclaim command + checkout).

This script does NOT remove the worktree — the agent is standing in it.
The actual filesystem cleanup happens when the harness reaps the agent
session, or via ``/cstack-collab:reclaim`` from the primary repo.

Exit codes:
    0   success
    1   not inside an agent worktree
    2   dirty tree without an action flag, or other usage error
"""

from __future__ import annotations

import argparse
import json
import os
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


def _find_self() -> wt.Worktree | None:
    """Return the agent-worktree record matching the current cwd, if any."""
    cwd = Path.cwd().resolve()
    try:
        worktrees = wt.discover()
    except subprocess.CalledProcessError:
        return None
    for w in worktrees:
        if Path(w.path).resolve() == cwd or cwd.is_relative_to(Path(w.path).resolve()):
            return w
    return None


def _commit_all(message: str) -> str:
    _run(["git", "add", "-A"])
    _run(["git", "commit", "-m", message])
    return _run(["git", "rev-parse", "HEAD"]).strip()


def _stash_to_ref(agent_id: str) -> str:
    sha = _run(["git", "stash", "create", f"cstack-collab handoff {agent_id}"]).strip()
    if not sha:
        return ""
    ref = f"refs/cstack-collab/handoff/{agent_id}"
    _run(["git", "update-ref", ref, sha])
    _run(["git", "reset", "--hard", "HEAD"])
    _run(["git", "clean", "-fd"])
    return ref


def _state_path() -> Path | None:
    """Locate state.json (walks up from cwd). Returns None if not found."""
    here = Path(__file__).with_name("state.py")
    out = subprocess.run(
        [str(here), "find"], text=True, capture_output=True
    )
    if out.returncode != 0:
        return None
    p = out.stdout.strip()
    return Path(p) if p else None


def _append_event(state_path: Path, event: dict) -> None:
    data = json.loads(state_path.read_text())
    data.setdefault("events", []).append(event)
    state_path.write_text(json.dumps(data, indent=2) + "\n")


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    g = p.add_mutually_exclusive_group()
    g.add_argument("--commit", metavar="MSG", help="commit dirty state with this message")
    g.add_argument(
        "--stash",
        action="store_true",
        help="move dirty state to refs/cstack-collab/handoff/<agent-id>",
    )
    g.add_argument(
        "--discard",
        action="store_true",
        help="throw away the dirty state",
    )
    p.add_argument(
        "--push",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="push the branch to origin so the human can fetch without the worktree (default: yes)",
    )
    p.add_argument(
        "--summary",
        default="",
        help="one-line summary recorded in state.json events (orchestration only)",
    )
    args = p.parse_args(argv)

    self_w = _find_self()
    if self_w is None:
        print(
            "error: handoff must be run from inside a Claude agent worktree. "
            "If you want to take over a branch from the primary repo, use "
            "/cstack-collab:reclaim instead.",
            file=sys.stderr,
        )
        return 1

    if self_w.dirty:
        if args.commit:
            sha = _commit_all(args.commit)
            print(f"committed dirty state at {sha[:12]}")
        elif args.stash:
            ref = _stash_to_ref(self_w.agent_id or "agent")
            if ref:
                print(f"stashed dirty state at {ref}")
            else:
                print("nothing to stash (state was clean after all)")
        elif args.discard:
            _run(["git", "reset", "--hard", "HEAD"])
            _run(["git", "clean", "-fd"])
            print("discarded dirty state")
        else:
            print(
                "refusing to hand off with a dirty tree. Pass one of:\n"
                '  --commit "<message>"   commit the changes on this branch\n'
                "  --stash                preserve as refs/cstack-collab/handoff/<id>\n"
                "  --discard              throw the changes away",
                file=sys.stderr,
            )
            print(file=sys.stderr)
            sys.stderr.write(_run(["git", "status", "--short"]))
            return 2

    branch = self_w.branch
    head = _run(["git", "rev-parse", "HEAD"]).strip()

    pushed = False
    if args.push and branch:
        # Best-effort push. Don't fail handoff if push fails — the human
        # can still reclaim the worktree and pick up the branch locally.
        out = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            text=True,
            capture_output=True,
        )
        if out.returncode == 0:
            pushed = True
            print(f"pushed {branch} to origin")
        else:
            print(f"warning: push failed ({out.stderr.strip()})", file=sys.stderr)

    state_file = _state_path()
    if state_file is not None:
        _append_event(
            state_file,
            {
                "event": "handoff",
                "agent_id": self_w.agent_id,
                "branch": branch,
                "head": head,
                "summary": args.summary,
                "pushed": pushed,
                "at": datetime.now(timezone.utc).isoformat(),
            },
        )

    print()
    print("Handoff complete. Branch is ready for human review.")
    print(f"  branch: {branch}")
    print(f"  head:   {head[:12]}")
    print()
    print("Next steps for the human (run from the primary repo):")
    print(f"  /cstack-collab:reclaim {self_w.agent_id} --checkout")
    print("    (or, if you want the agent to keep working: do nothing — the")
    print("     branch stays on this worktree and the agent stays alive.)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
