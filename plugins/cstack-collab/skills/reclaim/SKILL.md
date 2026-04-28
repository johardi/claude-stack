---
name: reclaim
description: Run from the primary repo to take back a branch held by a Claude agent worktree (rescue mode). Locates the worktree by branch name or agent id, preserves any dirty state to a recovery ref, releases the lock, removes the worktree, and optionally checks out the branch. Use when the user types `/cstack-collab:reclaim <ref>`, or says things like "the agent worktree is stuck", "force-free this branch", "the agent died, give me the branch back", "I want to check out feature/X but git says it's already used by a worktree". Refuses by default if the agent's PID is still alive — the live agent should `/cstack-collab:handoff` instead.
allowed-tools: Bash, Read
---

# Reclaim

The complement to `handoff`. Where handoff is collaborative (live agent yields branch), reclaim is unilateral (human takes branch back without — or against — the agent's cooperation). Run from the primary repo, not from inside a worktree.

## When to Use

Use when:
- The user types `/cstack-collab:reclaim <branch-or-agent-id>` with optional flags.
- The user describes a stuck agent worktree: "the agent crashed", "the worktree is locked but the session is dead", "I can't check out feature/X — git says it's used by another worktree".
- An orchestrate-tickets wave left an agent worktree behind that needs to be cleaned up before the next wave.

Skip when:
- The agent is alive and reachable. Tell the user to type `/cstack-collab:handoff` in the agent's session instead — handoff preserves the agent's context and lets it write a meaningful commit message. Reclaim is the rescue tool, not the default.
- The user just wants to *list* what's stuck — that's `/cstack-collab:list-worktrees`.

## Inputs

| Argument | Meaning |
|---|---|
| `<ref>` (positional, required) | Branch name (`feature/66-x`), agent id (`agent-a81ac7c0…`), or absolute path to the worktree. |
| `--force` | Remove even when the agent's PID is still alive. **Kills the live agent's session.** Only pass when the user has explicitly acknowledged this — e.g., "the agent is wedged, just kill it". |
| `--stash` | (default) preserve dirty state at `refs/cstack-collab/reclaim/<agent-id>`. |
| `--discard` | Throw the dirty state away. |
| `--checkout` | After removal, run `git checkout <branch>` in the primary repo. |

## How to Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/reclaim.py" <ref> [flags]
```

The script:
1. Locates the agent worktree. Refuses if the ref doesn't match exactly one.
2. Refuses if the agent's PID is alive, unless `--force` was passed.
3. Stashes any dirty state to `refs/cstack-collab/reclaim/<id>` (unless `--discard`). The ref points at a real commit object, so it survives `git worktree remove` — recover with `git stash apply <ref>` or `git cherry-pick <ref>`.
4. `git worktree unlock` + `git worktree remove [--force]`.
5. Optional `git checkout <branch>` in the primary repo.
6. Appends a `reclaimed` event to `state.json` if an orchestration is active.

## Decision Helper

Before invoking reclaim, ask: **"Is the agent alive?"**

- Run `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py" inspect <ref>`.
- If `lock: locked (pid <N> alive)` → tell the user to use handoff in the agent's session unless they've explicitly said the agent is wedged or they want to kill it.
- If `lock: locked (pid <N> dead — stale lock)` or `unlocked` → reclaim is the right tool; proceed.

## After the Script Runs

Tell the user:
- Where any dirty state went (`refs/cstack-collab/reclaim/<id>`) and how to recover it.
- That the worktree is gone and the branch is free.
- If `--checkout` was used: that the primary repo is now on that branch.
- If they wanted to keep working on the branch but didn't pass `--checkout`: the explicit checkout command.

## Don't

- Don't `--force` without a clear signal from the user. A live agent under reclaim dies mid-thought — that's a real cost.
- Don't reclaim a worktree that isn't a Claude agent worktree (the script filters by `claude agent` lock marker / `CLAUDE_BASE` file; if it doesn't match, the user is asking about something this skill doesn't manage).
- Don't reach for reclaim when handoff would do. Default to handoff; escalate to reclaim only when the agent can't do it.
