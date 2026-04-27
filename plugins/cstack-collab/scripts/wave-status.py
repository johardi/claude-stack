#!/usr/bin/env python3
"""Report merge state for a wave's PRs and (optionally) sync state.json.

Two ways to invoke:

    wave-status.py <pr1> <pr2> ...       # ad-hoc, just report
    wave-status.py --sync                # read PR list from state.json,
                                          # update merged=true in state.json
                                          # for every PR that has merged.

PR arguments may be URLs (`https://.../pull/123`), `#123`, or `123`.

Per PR, queries `gh pr view --json number,state,mergedAt,url`. The result
is a JSON array on stdout with one object per PR, plus an exit code that
summarizes the wave:

    0   every input PR is merged
    1   some PR is still open
    2   some PR was closed without merging (needs human attention)
    3   usage / fetch error

This is the gate the orchestrator uses to decide whether to release the
next wave. Keeping it as a script (instead of asking the model to
interpret `gh` output) means the gate is deterministic.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# state.py lives in the same directory; let it find its own state file.
HERE = Path(__file__).resolve().parent
STATE_PY = HERE / "state.py"


def normalize_pr(arg: str) -> str:
    """Accept URL, '#123', or '123'. Return whatever `gh pr view` accepts.

    `gh pr view` accepts URL or number; pass URL through, numbers as-is.
    """
    if arg.startswith("http"):
        return arg
    return arg.lstrip("#")


def gh_pr_view(pr: str) -> dict:
    try:
        out = subprocess.check_output(
            ["gh", "pr", "view", pr,
             "--json", "number,state,mergedAt,url,title"],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        msg = e.stderr.decode().strip() or f"gh exit {e.returncode}"
        print(f"error: cannot view PR {pr}: {msg}", file=sys.stderr)
        sys.exit(3)
    return json.loads(out)


def state_pending_prs() -> list[str]:
    """Read state.json and return PR URLs (or fall back to PR numbers) for
    every child whose merged flag is False but which has a recorded PR."""
    try:
        out = subprocess.check_output([str(STATE_PY), "get", "results"])
    except subprocess.CalledProcessError as e:
        print("error: no active orchestration state", file=sys.stderr)
        sys.exit(3)
    results = json.loads(out)
    return [
        entry["pr"]
        for entry in results.values()
        if entry.get("pr") and not entry.get("merged")
    ]


def state_mark_merged(pr_url: str) -> None:
    """Update state.json: set the matching child's merged=true."""
    out = subprocess.check_output([str(STATE_PY), "get", "results"])
    results = json.loads(out)
    target = _pr_number_from_url(pr_url)
    for issue, entry in results.items():
        if entry.get("pr") and _pr_number_from_url(entry["pr"]) == target:
            entry["merged"] = True
    subprocess.check_call(
        [str(STATE_PY), "set", "results", json.dumps(results)]
    )


def _pr_number_from_url(url: str) -> int | None:
    m = re.search(r"/pull/(\d+)", url)
    return int(m.group(1)) if m else None


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("prs", nargs="*", help="PR URLs, #N, or N")
    p.add_argument("--sync", action="store_true",
                   help="read PR list from state.json and update merged flags")
    args = p.parse_args(argv)

    if args.sync and args.prs:
        print("error: --sync takes no positional args", file=sys.stderr)
        return 3
    if not args.sync and not args.prs:
        print("error: pass PR list or --sync", file=sys.stderr)
        return 3

    targets = state_pending_prs() if args.sync else [normalize_pr(x) for x in args.prs]
    if not targets:
        print(json.dumps([], indent=2))
        return 0

    statuses = []
    for pr in targets:
        info = gh_pr_view(pr)
        merged = info["state"] == "MERGED" and info.get("mergedAt") is not None
        statuses.append({
            "number": info["number"],
            "url": info["url"],
            "title": info.get("title"),
            "state": info["state"],
            "merged": merged,
        })
        if args.sync and merged:
            state_mark_merged(info["url"])

    print(json.dumps(statuses, indent=2))

    if any(s["state"] == "CLOSED" and not s["merged"] for s in statuses):
        return 2
    if all(s["merged"] for s in statuses):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
