#!/usr/bin/env python3
"""Lint a compose-tickets body for structural conformance.

Catches the format-level mistakes that confuse orchestrate-tickets and
build-dag.py — most importantly, dependency phrases without an explicit
'#N' (e.g. "Depends on the data-model unification sub-ticket"), and
missing required sections.

Usage:
    lint-ticket.py < body.md                 # read from stdin
    lint-ticket.py --file body.md            # read from file
    lint-ticket.py --type child --file ...   # force ticket type

Auto-detects parent vs child from the body:
    Sub-ticket of #N  -> child
    ## Tracking + checklist of #N -> parent

Exit codes:
    0   conforming
    2   one or more violations (printed to stderr, one per line)
    3   usage error
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import List

# Sections required per ticket type, by canonical name. The pattern matches
# the corresponding "## Heading" line, allowing some spelling flexibility
# (e.g., "Out of Scope" vs "Out-of-Scope", "Test" vs "Tests").
SECTION_PATTERNS = {
    "Problem":           re.compile(r"^##\s+problem\b",                re.IGNORECASE | re.MULTILINE),
    "Analysis":          re.compile(r"^##\s+analysis\b",               re.IGNORECASE | re.MULTILINE),
    "Proposed Solution": re.compile(r"^##\s+proposed\s+solution\b",    re.IGNORECASE | re.MULTILINE),
    "Tests":             re.compile(r"^##\s+tests?\b",                 re.IGNORECASE | re.MULTILINE),
    "Out of Scope":      re.compile(r"^##\s+out[\s\-]+of[\s\-]+scope\b", re.IGNORECASE | re.MULTILINE),
    "Tracking":          re.compile(r"^##\s+tracking\b",               re.IGNORECASE | re.MULTILINE),
}

CHILD_REQUIRED  = ["Problem", "Analysis", "Proposed Solution", "Tests", "Out of Scope"]
PARENT_REQUIRED = ["Tracking"]

SUB_TICKET_RE = re.compile(r"\bsub[\-\s]?ticket\s+of\s+#(\d+)", re.IGNORECASE)
CHECKLIST_RE  = re.compile(r"^\s*-\s*\[[ xX]\]\s*#(\d+)", re.MULTILINE)
HASH_NUM_RE   = re.compile(r"#\d+")

# Match a dependency phrase that introduces a relationship to another ticket.
# The point of the linter is to ensure such a phrase carries a #N.
# Use \b boundaries so we don't match inside words like "undepends".
DEP_PHRASE_RE = re.compile(
    r"\b(?:depends\s+on|depends:|blocked\s+by|blocked:)",
    re.IGNORECASE,
)

# Crude sentence splitter — good enough for issue prose. Splits on
# sentence-ending punctuation followed by whitespace, plus newlines.
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")


def detect_type(body: str) -> str:
    if SUB_TICKET_RE.search(body):
        return "child"
    if SECTION_PATTERNS["Tracking"].search(body):
        return "parent"
    return "unknown"


def check_required_sections(body: str, names: list[str]) -> list[str]:
    out = []
    for name in names:
        if not SECTION_PATTERNS[name].search(body):
            out.append(f"missing required section: ## {name}")
    return out


def check_dependency_markers(body: str) -> list[str]:
    """Every dependency phrase must include a #N in the same sentence."""
    out = []
    for sent in SENTENCE_SPLIT_RE.split(body):
        sent_stripped = sent.strip()
        if not sent_stripped:
            continue
        if DEP_PHRASE_RE.search(sent_stripped) and not HASH_NUM_RE.search(sent_stripped):
            snippet = sent_stripped if len(sent_stripped) <= 100 else sent_stripped[:97] + "..."
            out.append(f"dependency phrase without #N: {snippet!r}")
    return out


def check_child(body: str) -> list[str]:
    out: list[str] = []
    if not SUB_TICKET_RE.search(body):
        out.append("missing 'Sub-ticket of #N' reference")
    out += check_required_sections(body, CHILD_REQUIRED)
    return out


def check_parent(body: str) -> list[str]:
    out: list[str] = []
    out += check_required_sections(body, PARENT_REQUIRED)
    if not CHECKLIST_RE.search(body):
        out.append("Tracking section has no '- [ ] #N' checklist items")
    return out


def lint(body: str, ticket_type: str) -> list[str]:
    if ticket_type == "auto":
        ticket_type = detect_type(body)

    violations: list[str] = []
    if ticket_type == "child":
        violations += check_child(body)
    elif ticket_type == "parent":
        violations += check_parent(body)
    elif ticket_type == "unknown":
        violations.append(
            "could not auto-detect ticket type "
            "(no 'Sub-ticket of #N' and no '## Tracking' section). "
            "Pass --type child|parent if this body is intentional."
        )
    # Dependency-phrase check applies to every ticket type.
    violations += check_dependency_markers(body)
    return violations


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--file", help="markdown file to lint (default: stdin)")
    p.add_argument("--type", choices=["child", "parent", "auto"], default="auto")
    args = p.parse_args(argv)

    if args.file:
        try:
            body = open(args.file).read()
        except OSError as e:
            print(f"lint-ticket: {e}", file=sys.stderr)
            return 3
    else:
        body = sys.stdin.read()

    if not body.strip():
        print("lint-ticket: empty body", file=sys.stderr)
        return 3

    violations = lint(body, args.type)
    if violations:
        for v in violations:
            print(f"lint-ticket: {v}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
