#!/usr/bin/env python3
"""CRUD over .cstack-collab/state.json — the active orchestration state file.

Used by both the orchestrate-tickets skill and the plugin's hooks. The state
file is repo-scoped: scripts walk up from $PWD looking for .cstack-collab/
the same way `git` finds `.git`.

Subcommands:
    init <parent> <wave-json> <default-branch>
        Create state.json for a fresh orchestration. Refuses if one already
        exists for that parent.

    find
        Print the absolute path to the active state file, or exit 1 if none.

    get <key> [--state PATH]
        Read a top-level field (parent, wave_index, waves, results,
        default_branch). JSON-encoded output.

    set <key> <json-value> [--state PATH]
        Overwrite a top-level field with a JSON value.

    append-result <issue> <pr-url> <branch> [--state PATH]
        Record a worker result. Idempotent on (issue).

    is-child <pr-url> [--state PATH]
        Exit 0 if the PR belongs to the active orchestration, 1 otherwise.

    is-parent <issue> [--state PATH]
        Exit 0 if the given issue number is the active parent, 1 otherwise.

    pending-children [--state PATH]
        Print issue numbers (one per line) of children whose result is not
        yet merged. Empty output means the wave/orchestration is complete.

    complete [--state PATH]
        Move state.json to state.completed.json once everything is merged.

State file shape:
    {
        "parent": 64,
        "default_branch": "main",
        "waves": [[65, 66], [67, 68]],
        "wave_index": 0,
        "results": {
            "65": {"pr": "https://.../pull/120", "branch": "feature/65-x", "merged": true},
            ...
        }
    }

Exit codes:
    0   success
    1   not found / negative answer
    2   usage / validation error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STATE_DIRNAME = ".cstack-collab"
STATE_FILENAME = "state.json"


def find_state_dir(start: Path | None = None) -> Path | None:
    """Walk up from `start` (default $PWD) looking for .cstack-collab/."""
    cur = (start or Path.cwd()).resolve()
    for parent in [cur, *cur.parents]:
        candidate = parent / STATE_DIRNAME
        if candidate.is_dir():
            return candidate
    return None


def find_state_file(start: Path | None = None) -> Path | None:
    d = find_state_dir(start)
    if not d:
        return None
    f = d / STATE_FILENAME
    return f if f.is_file() else None


def load_state(path: Path) -> dict:
    return json.loads(path.read_text())


def save_state(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def resolve_state_path(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    found = find_state_file()
    if not found:
        print("error: no active orchestration state found", file=sys.stderr)
        sys.exit(1)
    return found


def cmd_init(args: argparse.Namespace) -> int:
    waves = json.loads(args.waves)
    if not isinstance(waves, list) or not all(
        isinstance(w, list) and all(isinstance(n, int) for n in w) for w in waves
    ):
        print("error: --waves must be JSON list of lists of ints", file=sys.stderr)
        return 2
    state_dir = Path.cwd() / STATE_DIRNAME
    state_path = state_dir / STATE_FILENAME
    if state_path.exists():
        print(f"error: state already exists at {state_path}", file=sys.stderr)
        return 2
    data = {
        "parent": args.parent,
        "default_branch": args.default_branch,
        "waves": waves,
        "wave_index": 0,
        "results": {str(n): {"pr": None, "branch": None, "merged": False}
                    for w in waves for n in w},
    }
    save_state(state_path, data)
    print(str(state_path))
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    f = find_state_file()
    if not f:
        return 1
    print(str(f))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    if args.key not in data:
        print(f"error: unknown key {args.key!r}", file=sys.stderr)
        return 2
    print(json.dumps(data[args.key]))
    return 0


def cmd_set(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    data[args.key] = json.loads(args.value)
    save_state(path, data)
    return 0


def cmd_append_result(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    key = str(args.issue)
    if key not in data["results"]:
        print(f"error: issue #{args.issue} is not part of this orchestration",
              file=sys.stderr)
        return 2
    entry = data["results"][key]
    entry["pr"] = args.pr_url
    entry["branch"] = args.branch
    save_state(path, data)
    return 0


def _pr_number_from_url(url: str) -> int | None:
    m = re.search(r"/pull/(\d+)", url)
    return int(m.group(1)) if m else None


def cmd_is_child(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    target = _pr_number_from_url(args.pr_url) if args.pr_url.startswith("http") else None
    raw_target = args.pr_url.lstrip("#")
    try:
        raw_target_int = int(raw_target)
    except ValueError:
        raw_target_int = None
    for entry in data["results"].values():
        if not entry.get("pr"):
            continue
        n = _pr_number_from_url(entry["pr"])
        if n is None:
            continue
        if target is not None and n == target:
            return 0
        if raw_target_int is not None and n == raw_target_int:
            return 0
        if entry["pr"] == args.pr_url:
            return 0
    return 1


def cmd_is_parent(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    raw = str(args.issue).lstrip("#")
    try:
        n = int(raw)
    except ValueError:
        return 2
    return 0 if data["parent"] == n else 1


def cmd_pending_children(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    for issue, entry in data["results"].items():
        if not entry.get("merged"):
            print(issue)
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    path = resolve_state_path(args.state)
    data = load_state(path)
    if any(not e.get("merged") for e in data["results"].values()):
        print("error: cannot complete — children still pending", file=sys.stderr)
        return 2
    done = path.with_name("state.completed.json")
    path.rename(done)
    print(str(done))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init", help="create a new state file in $PWD/.cstack-collab/")
    s.add_argument("--parent", type=int, required=True)
    s.add_argument("--waves", required=True,
                   help='JSON list of lists of ints, e.g. "[[65,66],[67,68]]"')
    s.add_argument("--default-branch", required=True)
    s.set_defaults(func=cmd_init)

    s = sub.add_parser("find", help="print path to active state.json or exit 1")
    s.set_defaults(func=cmd_find)

    s = sub.add_parser("get", help="read a top-level field")
    s.add_argument("key")
    s.add_argument("--state")
    s.set_defaults(func=cmd_get)

    s = sub.add_parser("set", help="overwrite a top-level field")
    s.add_argument("key")
    s.add_argument("value", help="JSON value")
    s.add_argument("--state")
    s.set_defaults(func=cmd_set)

    s = sub.add_parser("append-result", help="record a worker result")
    s.add_argument("--issue", type=int, required=True)
    s.add_argument("--pr-url", required=True)
    s.add_argument("--branch", required=True)
    s.add_argument("--state")
    s.set_defaults(func=cmd_append_result)

    s = sub.add_parser("is-child", help="exit 0 if pr belongs to active orchestration")
    s.add_argument("pr_url", help="PR URL or PR number (#123 or 123)")
    s.add_argument("--state")
    s.set_defaults(func=cmd_is_child)

    s = sub.add_parser("is-parent", help="exit 0 if issue is the active parent")
    s.add_argument("issue", help="issue number (#64 or 64)")
    s.add_argument("--state")
    s.set_defaults(func=cmd_is_parent)

    s = sub.add_parser("pending-children", help="list unmerged child issue numbers")
    s.add_argument("--state")
    s.set_defaults(func=cmd_pending_children)

    s = sub.add_parser("complete",
                       help="rename state.json to state.completed.json")
    s.add_argument("--state")
    s.set_defaults(func=cmd_complete)

    return p


def main(argv: list[str]) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
