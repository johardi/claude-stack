#!/usr/bin/env python3
"""Build a wave-ordered DAG from a set of GitHub issue numbers.

For each input issue, fetches the body via `gh`, extracts dependency
markers, topologically sorts into waves, refuses cycles, and emits JSON.

Recognized dependency markers (case-insensitive, anywhere in the body):
    Depends on #N
    Depends: #N
    Blocked by #N
    Blocked: #N

`Sub-ticket of #N` and `Parent: #N` are deliberately NOT treated as
dependencies — they are informational backlinks. Including them as edges
would forbid running children before the parent issue closes, which is
the opposite of what we want.

Inputs:
    - One or more issue numbers as positional args, OR
    - A single parent issue via --parent <N>: in which case child issues
      are extracted from the parent's checklist (lines like
      "- [ ] #N — ..." or "- [x] #N — ..."). The parent itself is not
      included as a node in the DAG; it becomes the "parent" field on
      the output.

Output (stdout, JSON):
    {
        "parent": <int or null>,
        "issues": [<int>, ...],          # all node ids, deduped, sorted
        "edges": [[from, to], ...],       # "from depends on to"
        "waves": [[<int>, ...], ...]      # topo order, one list per wave
    }

Exit codes:
    0   success
    1   cycle detected
    2   usage / fetch error
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from typing import Iterable

DEP_RE = re.compile(
    r"\b(?:depends\s+on|depends|blocked\s+by|blocked)\s*[:\-]?\s*#(\d+)",
    re.IGNORECASE,
)
CHECKLIST_RE = re.compile(r"^\s*-\s*\[[ xX]\]\s*#(\d+)", re.MULTILINE)


def gh_issue_body(issue: int) -> str:
    """Fetch the body of an issue with `gh`. Returns "" if the body is null."""
    try:
        out = subprocess.check_output(
            ["gh", "issue", "view", str(issue), "--json", "body", "--jq", ".body // \"\""],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        msg = e.stderr.decode().strip() or f"gh exit {e.returncode}"
        print(f"error: cannot fetch issue #{issue}: {msg}", file=sys.stderr)
        sys.exit(2)
    return out.decode()


def extract_deps(body: str, valid_nodes: set[int]) -> set[int]:
    """Return the set of issue numbers this body depends on.

    Filters to `valid_nodes` so a stray "Depends on #999" referring to an
    issue outside the orchestration doesn't poison the DAG.
    """
    found = {int(m) for m in DEP_RE.findall(body)}
    return found & valid_nodes


def extract_checklist_children(body: str) -> list[int]:
    return [int(m) for m in CHECKLIST_RE.findall(body)]


def topo_waves(nodes: list[int], edges: list[tuple[int, int]]) -> list[list[int]]:
    """Kahn's algorithm, grouped by wave.

    Wave 0 = every node with no in-edges; wave i = every node whose
    dependencies are all in waves < i. Sorts within a wave for stability.
    """
    indeg: dict[int, int] = {n: 0 for n in nodes}
    out_edges: dict[int, list[int]] = defaultdict(list)
    for a, b in edges:
        indeg[a] += 1
        out_edges[b].append(a)
    waves: list[list[int]] = []
    remaining = set(nodes)
    while remaining:
        layer = sorted(n for n in remaining if indeg[n] == 0)
        if not layer:
            cycle = sorted(remaining)
            print(f"error: dependency cycle among issues {cycle}", file=sys.stderr)
            sys.exit(1)
        waves.append(layer)
        for n in layer:
            remaining.discard(n)
            for downstream in out_edges[n]:
                indeg[downstream] -= 1
    return waves


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("issues", nargs="*", type=int,
                   help="explicit list of issue numbers")
    p.add_argument("--parent", type=int,
                   help="extract children from this parent's checklist")
    args = p.parse_args(argv)

    if args.parent and args.issues:
        print("error: pass either positional issues OR --parent, not both",
              file=sys.stderr)
        return 2
    if not args.parent and not args.issues:
        print("error: no issues given", file=sys.stderr)
        return 2

    if args.parent:
        parent_body = gh_issue_body(args.parent)
        nodes = sorted(set(extract_checklist_children(parent_body)))
        if not nodes:
            print(f"error: parent #{args.parent} has no checklist children",
                  file=sys.stderr)
            return 2
    else:
        nodes = sorted(set(args.issues))

    valid = set(nodes)
    edges: list[tuple[int, int]] = []
    for n in nodes:
        body = gh_issue_body(n)
        for dep in extract_deps(body, valid):
            if dep != n:
                edges.append((n, dep))  # n depends on dep

    waves = topo_waves(nodes, edges)

    print(json.dumps({
        "parent": args.parent,
        "issues": nodes,
        "edges": edges,
        "waves": waves,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
