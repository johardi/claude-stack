---
name: handoff
description: Run inside a Claude agent worktree to yield the branch back to the human. Commits, stashes, or discards any dirty state, optionally pushes the branch to origin, records a handoff event in state.json (when an orchestration is active), and prints next-step instructions so the human can `/cstack-collab:reclaim` and check out the branch in their primary repo. Use when the human types `/cstack-collab:handoff` during an active agent session and signals they want to take over the branch — typical phrasings include "let's hand off", "I'll take over", "give me the branch", "finish cleanly so I can review locally". Do NOT use to clean up someone else's worktree from the primary repo — that's `/cstack-collab:reclaim`.
allowed-tools: Bash, Read
---

# Handoff

The agent is standing in an isolated worktree (created by `Agent({isolation: "worktree"})` or by `cstack-collab` orchestration). The human wants to take the branch over locally — review the actual files, run a dev server, etc. — without waiting for a PR merge or the harness's automatic worktree reaping.

This skill is the agent's "I'm yielding" ritual. It does not remove the worktree (the agent is standing in it); it puts the branch in a state where the human can pick it up cleanly via `/cstack-collab:reclaim`.

## When to Use

Use when:
- The human types `/cstack-collab:handoff` (with optional flags).
- The human says something equivalent during an active agent session: "let's hand off", "I'll take over", "wrap up so I can check out the branch", "finish cleanly".

Skip when:
- Not inside a Claude agent worktree. The script will refuse anyway, but recognize this up front and route the human to `/cstack-collab:reclaim` instead.
- The human is asking the agent to *commit* its work but keep working — that's just a normal commit, not a handoff.

## Inputs

The human may pass any of these (interpret natural language too — e.g., "stash my changes" → `--stash`):

| Flag | Meaning |
|---|---|
| `--commit "<msg>"` | Commit dirty state on the current branch with this message. Default if you can derive a meaningful message from the conversation. |
| `--stash` | Preserve dirty state at `refs/cstack-collab/handoff/<agent-id>` instead of committing. |
| `--discard` | Throw the dirty state away. |
| `--no-push` | Skip the `git push -u origin <branch>` step. Default is to push. |
| `--summary "<text>"` | One-line summary recorded in `state.json` events (orchestration only). |

If the tree is dirty and none of `--commit`, `--stash`, `--discard` is supplied, the script refuses. **Do not silently pick one for the user** — ask them which they want, citing the changed files.

## How to Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/handoff.py" [flags]
```

The script:
1. Refuses if not inside a Claude agent worktree.
2. Handles dirty state per the flag (commit / stash / discard).
3. Best-effort `git push -u origin <branch>` (override with `--no-push`).
4. Appends a `handoff` event to `state.json` if an orchestration is active.
5. Prints the exact `/cstack-collab:reclaim` invocation the human should run from their primary repo.

## After the Script Runs

Tell the human, in plain English:
- What happened to dirty state (committed at `<sha>` / stashed at `<ref>` / discarded).
- Whether the push succeeded.
- The exact reclaim command to run from the primary repo.
- That the agent's session will be ended by the harness when this turn returns; if the human prefers to force-remove sooner, they can run reclaim immediately.

Do not call `ExitWorktree` afterward — that tool only operates on `EnterWorktree`-created worktrees, not harness-created agent isolation worktrees, and is a no-op here.

## Don't

- Don't run handoff from the primary repo "to be helpful" — it's defensive about that and will refuse.
- Don't run handoff when the human is asking for a commit-and-continue workflow. That's just `git commit`.
- Don't auto-merge the branch or open a PR as part of handoff. PR creation belongs to `github-issue-workflow`.
