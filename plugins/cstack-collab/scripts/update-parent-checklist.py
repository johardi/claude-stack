#!/usr/bin/env python3
"""Idempotent updater for a parent issue's tracking checklist.

Reads the parent issue body, toggles `- [ ] #N` to `- [x] #N` for each
child whose merged flag is true in state.json (or for the children passed
explicitly on the command line), and writes the body back via
`gh issue edit --body-file -`.

Embeds a marker comment in the body so the deny-parent-mutations hook
can recognize body edits made by this script as legitimate. The marker
is harmless to GitHub's renderer (it's an HTML comment) and is preserved
across edits.

Usage:
    update-parent-checklist.py --from-state
        Reads the parent issue + merged children from .cstack-collab/state.json.

    update-parent-checklist.py --parent 64 --merged 65 --merged 66
        Explicit. Useful for ad-hoc fixes outside the orchestrator.

    update-parent-checklist.py --parent 64 --from-state --dry-run
        Print the resulting body to stdout instead of pushing.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATE_PY = HERE / "state.py"

MARKER = "<!-- cstack-collab:checklist -->"

# Match a checklist line referencing #N. Capture indent, current state, and N.
LINE_RE = re.compile(
    r"^(?P<indent>\s*)-\s*\[(?P<state>[ xX])\]\s*#(?P<n>\d+)\b",
    re.MULTILINE,
)


def gh_get_body(issue: int) -> str:
    out = subprocess.check_output(
        ["gh", "issue", "view", str(issue), "--json", "body", "--jq", ".body // \"\""]
    )
    return out.decode()


def gh_set_body(issue: int, body: str) -> None:
    proc = subprocess.run(
        ["gh", "issue", "edit", str(issue), "--body-file", "-"],
        input=body, text=True, capture_output=True,
    )
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        sys.exit(2)


def ensure_marker(body: str) -> str:
    """Add the marker on its own line at end-of-body if absent."""
    if MARKER in body:
        return body
    sep = "" if body.endswith("\n") else "\n"
    return f"{body}{sep}\n{MARKER}\n"


def toggle_lines(body: str, merged: set[int]) -> tuple[str, list[int]]:
    """Return (new_body, list-of-issue-numbers-actually-toggled)."""
    toggled: list[int] = []

    def repl(m: re.Match[str]) -> str:
        n = int(m.group("n"))
        cur = m.group("state")
        if n in merged and cur == " ":
            toggled.append(n)
            return f"{m.group('indent')}- [x] #{n}"
        return m.group(0)

    return LINE_RE.sub(repl, body), toggled


def from_state() -> tuple[int, set[int]]:
    """Return (parent, set of merged children) from state.json."""
    parent = int(json.loads(
        subprocess.check_output([str(STATE_PY), "get", "parent"])
    ))
    results = json.loads(
        subprocess.check_output([str(STATE_PY), "get", "results"])
    )
    merged = {int(k) for k, v in results.items() if v.get("merged")}
    return parent, merged


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--parent", type=int)
    p.add_argument("--merged", type=int, action="append", default=[])
    p.add_argument("--from-state", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    if args.from_state:
        parent, merged_set = from_state()
        if args.parent and args.parent != parent:
            print(f"error: --parent #{args.parent} does not match active state "
                  f"(parent #{parent})", file=sys.stderr)
            return 2
        merged_set |= set(args.merged)
    else:
        if not args.parent:
            print("error: --parent required when --from-state is not set",
                  file=sys.stderr)
            return 2
        parent = args.parent
        merged_set = set(args.merged)

    if not merged_set:
        print("error: nothing to mark merged", file=sys.stderr)
        return 2

    body = gh_get_body(parent)
    new_body, toggled = toggle_lines(body, merged_set)
    new_body = ensure_marker(new_body)

    if not toggled and new_body == body:
        # Nothing to do.
        print("noop: no checklist lines changed")
        return 0

    if args.dry_run:
        sys.stdout.write(new_body)
        return 0

    gh_set_body(parent, new_body)
    print(f"updated #{parent}: toggled {sorted(toggled)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
