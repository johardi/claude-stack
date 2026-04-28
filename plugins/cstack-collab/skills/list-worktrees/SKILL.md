---
name: list-worktrees
description: List all Claude agent worktrees in the current repo with branch, lock state (live agent / stale lock / unlocked), dirty/clean status, and unpushed commits. Use when the user types `/cstack-collab:list-worktrees`, or asks "what agent worktrees are open", "show me the stuck branches", "which agents are still running", "where's my work for feature/X". Read-only — never modifies state. Companion debugging tool for `/cstack-collab:handoff` and `/cstack-collab:reclaim`.
allowed-tools: Bash, Read
---

# List Worktrees

A read-only inventory of Claude agent worktrees — the worktrees created by `Agent({isolation: "worktree"})` or by `cstack-collab` orchestration. Used to figure out *which* worktrees exist before deciding what to do with them (`handoff` from inside, `reclaim` from outside).

## When to Use

Use when:
- The user types `/cstack-collab:list-worktrees`.
- The user asks for an overview: "what agents are running", "which branches are stuck", "show me the worktrees", "what's holding feature/X".
- Before invoking `handoff` or `reclaim` and the user hasn't named a specific worktree — list first, then ask.

Skip when:
- The user already named a specific branch / agent id and just wants to act on it. Go straight to `worktree.py inspect` or to `handoff` / `reclaim`.

## How to Run

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py" list
```

Or, for downstream scripting:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/worktree.py" list --json
```

Output shape (human-readable):

```
agent-<id>
  path:   <absolute path>
  branch: <branch name or "(detached)">
  lock:   unlocked | locked (pid N alive) | locked (pid N dead — stale lock)
  state:  clean | dirty | N unpushed | combinations
```

The script ignores plain user-created worktrees — only worktrees that carry the `claude agent <id>` lock marker or the `CLAUDE_BASE` file are listed.

## Interpreting the Output

| Lock | State | Recommendation |
|---|---|---|
| live PID | clean | Agent is working normally. Leave it alone. |
| live PID | dirty / unpushed | If the user wants to take the branch over: type `/cstack-collab:handoff` in that agent's session. Don't reclaim — it would kill the agent. |
| stale PID | clean | Safe to `/cstack-collab:reclaim` without flags. |
| stale PID | dirty / unpushed | `/cstack-collab:reclaim` (default `--stash`) preserves the work to a recovery ref. |
| unlocked | any | The harness has already released this. Reclaim removes the directory; nothing else to clean up. |

## Don't

- Don't try to filter or reformat the output for "interesting" entries — show the user everything the script returned. Surprises hide in the boring entries.
- Don't run `git worktree list` directly as a substitute. It includes user-created worktrees and lacks lock/dirty info; the wrapper is the source of truth for cstack-collab.
