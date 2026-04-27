#!/usr/bin/env python3
"""PostToolUse(Agent) hook: record a worker's PR result in state.json.

Best-effort. The worker is contractually obligated (per worker-prompt.sh)
to return a JSON object containing { issue, pr_url, branch, summary,
blockers }. This hook tries to find that object in the agent's response
text and append-result it into the active state.json so the orchestrator
doesn't need to remember to do it manually.

Failure modes are deliberately silent (exit 0):
    - no active state file               (not orchestrating)
    - tool isn't Agent                    (wrong matcher)
    - subagent name isn't `ticket-N`      (some other subagent)
    - response shape unrecognized         (worker drifted)
    - JSON parse failure                  (best-effort)

Hooks should not fail closed on PostToolUse — that would block legitimate
work. Recording is convenience, not enforcement.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def main() -> int:
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if not plugin_root:
        return 0  # not invoked by the harness — treat as no-op
    state_py = Path(plugin_root) / "scripts" / "state.py"

    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool_input = payload.get("tool_input") or {}
    if "subagent_type" not in tool_input:
        return 0
    name = tool_input.get("name") or ""
    m = re.fullmatch(r"ticket-(\d+)", name)
    if not m:
        return 0
    declared_issue = int(m.group(1))

    # Active state required.
    try:
        subprocess.check_output([str(state_py), "find"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return 0

    response = payload.get("tool_response")
    text = _extract_response_text(response)
    if not text:
        return 0

    obj = _find_worker_json(text)
    if not obj:
        return 0

    issue = obj.get("issue") or declared_issue
    pr_url = obj.get("pr_url")
    branch = obj.get("branch")
    if not pr_url or not branch:
        return 0

    try:
        subprocess.run(
            [str(state_py), "append-result",
             "--issue", str(issue),
             "--pr-url", str(pr_url),
             "--branch", str(branch)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        sys.stderr.write(
            f"cstack-collab: recorded worker result for #{issue} → {pr_url}\n"
        )
    except subprocess.CalledProcessError:
        pass

    return 0


def _extract_response_text(response: object) -> str:
    """Walk a few common shapes to find the agent's textual reply."""
    if response is None:
        return ""
    if isinstance(response, str):
        return response
    if isinstance(response, dict):
        for key in ("text", "summary", "content", "message"):
            v = response.get(key)
            if isinstance(v, str) and v:
                return v
            if isinstance(v, list):
                joined = " ".join(
                    item.get("text", "") if isinstance(item, dict) else str(item)
                    for item in v
                )
                if joined.strip():
                    return joined
        # Last resort: stringify the whole thing so the regex can still hunt.
        return json.dumps(response)
    if isinstance(response, list):
        joined = " ".join(_extract_response_text(item) for item in response)
        return joined
    return str(response)


def _find_worker_json(text: str) -> dict | None:
    """Find the first JSON object in `text` that contains a 'pr_url' key.

    The worker's reply is a JSON object embedded in possibly-prose. Brace
    matching is good-enough here because the contract object is shallow
    (no nested objects with their own `pr_url`).
    """
    # Pull every {...} candidate, broadest first.
    for match in re.finditer(r"\{[^{}]*\}", text, re.DOTALL):
        chunk = match.group(0)
        if '"pr_url"' not in chunk:
            continue
        try:
            return json.loads(chunk)
        except json.JSONDecodeError:
            continue
    return None


if __name__ == "__main__":
    sys.exit(main())
