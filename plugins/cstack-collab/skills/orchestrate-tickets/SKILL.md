---
name: orchestrate-tickets
description: Orchestrate a parent GitHub issue that has been broken into dependent sub-tickets, by spawning per-ticket workers in isolated git worktrees so each sub-ticket lands as its own PR. Use when the user wants to coordinate multiple related issues into separate PRs (e.g., "orchestrate #64", "run the sub-tickets for issue #N", "coordinate the work on these tickets", "fan out the children of this issue", "open separate PRs for these issues"). Builds an execution DAG from "Depends on #N" markers in issue bodies, runs independent tickets in parallel, serializes dependents, and pauses for the user to review and merge between waves. Never auto-merges. Pairs with the cstack-core github-issue-workflow skill for the per-ticket implementation.
allowed-tools: Bash, Read, Write, Edit, Agent, AskUserQuestion, TodoWrite
---

# Orchestrate Tickets

Multi-agent orchestration of a parent GitHub issue plus dependent sub-tickets. One PR per sub-ticket, with a human-in-the-loop merge gate between waves.

## When to Use

Use when:
- The user references a parent issue with sub-tickets (a checklist of `#N` items in the parent body).
- The user explicitly lists multiple issue numbers and asks for them to be coordinated.
- The user says: "orchestrate", "coordinate", "fan out", "run the sub-tickets", "open separate PRs for these".

Skip when:
- It is a single issue with no children → use the `github-issue-workflow` skill instead.
- The user wants a single PR that covers everything → use `github-issue-workflow` against the parent.

## How This Skill Stays Deterministic

Most of the work below is **delegated to scripts and hooks** that ship with this plugin. Treat their exit codes and stdout as the source of truth — do not paraphrase issue bodies, do not re-derive PR merge state from `gh` text output, do not hand-edit issue bodies. Specifically:

| Step | Tool |
|---|---|
| Preflight (gh, git, clean tree, default branch) | `${CLAUDE_PLUGIN_ROOT}/scripts/check-prereqs.sh` |
| Build the dependency DAG | `${CLAUDE_PLUGIN_ROOT}/scripts/build-dag.py` |
| Initialize / read / mutate state | `${CLAUDE_PLUGIN_ROOT}/scripts/state.py` |
| Render the worker prompt | `${CLAUDE_PLUGIN_ROOT}/scripts/worker-prompt.sh` |
| Check whether a wave's PRs are merged | `${CLAUDE_PLUGIN_ROOT}/scripts/wave-status.py` |
| Update the parent issue's checklist | `${CLAUDE_PLUGIN_ROOT}/scripts/update-parent-checklist.py` |

Hooks bundled with this plugin enforce the trickier invariants regardless of model behavior:

- `PreToolUse(Bash)` denies `gh pr merge` against any child PR while orchestration is active.
- `PreToolUse(Bash)` denies `gh issue close <PARENT>` while children are unmerged, and denies `gh issue edit <PARENT> --body` unless the body carries the `<!-- cstack-collab:checklist -->` marker emitted by `update-parent-checklist.py`.
- `PostToolUse(Agent)` records the worker's PR result in state.json automatically when the subagent is named `ticket-N`.
- `SessionStart` prints a one-line summary if an orchestration is in progress in the current repo.

All hooks are scoped to the active orchestration: outside of one (no `state.json` found), they are no-ops. The escape hatch is `CSTACK_COLLAB_OVERRIDE=1` in the env.

## Inputs

Accept one of:

1. **A parent issue number** (e.g., `64`). Pass to `build-dag.py --parent <N>` to discover children.
2. **An explicit list** of issue numbers. Pass to `build-dag.py <N1> <N2> ...`.

If invoked with no argument, ask the user via `AskUserQuestion`.

## Workflow

### Phase 1 — Preflight & Discover

1. Run `check-prereqs.sh`. If it exits non-zero, surface the error and stop.
   Capture stdout — that is the default branch name.
2. Run `build-dag.py` with the user's input. Capture the JSON output:
   `{parent, issues, edges, waves}`.
3. If `build-dag.py` reports a cycle (exit 1), surface it and stop.

### Phase 2 — Plan & Confirm

1. Present the DAG to the user via `AskUserQuestion`:
   - Show the wave assignment.
   - Options: "Approve and start wave 0", "Edit the order", "Cancel".
2. Heuristic note for the user: dependency edges come from `Depends on #N` / `Blocked by #N` markers in issue bodies only. If a dependency is described in prose ("depends on the data-model unification ticket") instead of a marker, `build-dag.py` will miss it. Ask the user to confirm the wave order is right before proceeding.
3. On approval: `state.py init --parent <P> --waves <waves-json> --default-branch <B>`.
   This is the signal that turns the hooks on.

### Phase 3 — Execute Wave

For each ticket in the current wave:

1. **Branch hygiene**: ensure the orchestrator's cwd has fetched origin recently (`git fetch --prune origin`). Workers run in their own worktrees — the harness branches them off whatever HEAD it sees, so a stale orchestrator cwd produces stale child branches.
2. **Spawn workers in parallel** by issuing one `Agent` tool call per ticket in a single message:
   - `subagent_type`: `"general-purpose"`.
   - `isolation`: `"worktree"`.
   - `name`: `"ticket-<N>"` — required so the `record-worker.py` hook recognizes the subagent and records its result.
   - `description`: short, e.g. `"Implement issue #<N>"`.
   - `prompt`: the output of `worker-prompt.sh <N> <PARENT> <DEFAULT-BRANCH>`. Do not write your own template.
3. Workers must follow the `github-issue-workflow` skill to do the implementation end-to-end. They return a JSON object with `{issue, pr_url, branch, summary, blockers}` (≤ 200 words).
4. The `record-worker.py` hook captures that result into state.json. You do **not** need to call `state.py append-result` yourself — but check `state.py get results` after the wave completes to confirm everything was recorded; if not, call `append-result` manually.
5. If any worker reports blockers, do **not** auto-fix. Surface them to the user.

### Phase 4 — Yield for Human Review

After a wave's `Agent` calls return:

1. Print a checklist for the user, one line per PR:
   ```
   Wave <N> complete. PRs to review:
   - [ ] #<N1> → <PR URL>
   - [ ] #<N2> → <PR URL>
   ```
2. Stop. Do **not** poll for merges. Do **not** start the next wave on your own.
3. Tell the user: "Reply when these are merged (or say 'continue') to release wave <N+1>."
4. End the turn.

When the user resumes:

- Run `wave-status.py --sync`. Exit 0 means everything in the prior wave is merged; the script also updates state.json's `merged` flags. Exit 1 means at least one is still open — ask the user how to proceed. Exit 2 means a PR was closed without merging — stop.
- On exit 0: bump `state.py set wave_index <next>` and advance to Phase 3.

### Phase 5 — Close Out

When `state.py pending-children` returns empty:

1. Run `update-parent-checklist.py --from-state` to flip any remaining `- [ ]` boxes to `- [x]`.
2. Post a closing comment on the parent issue listing the merged PRs.
3. Run `state.py complete` to move state.json to state.completed.json (this turns the hooks back into no-ops).
4. Ask the user whether to close the parent. Do **not** close it unilaterally — the deny-parent-mutations hook will block it anyway while children are still pending, but you should also respect user intent at this final step.

## Gotchas Baked In

- **Always branch off post-merge `<default-branch>` for dependents** — never off a sibling worker's branch.
- **Run independent tickets in parallel** by issuing multiple `Agent` tool calls in a single message. Serialize anything with a dependency edge.
- **No auto-merge.** The deny-merge hook is a backstop, but you should not be running `gh pr merge` at all.
- **Conflict policy**: a worker may rebase on `origin/<default-branch>` once. If the conflict persists, stop and report.
- **Test/lint failure policy**: workers stop on failures and report. They do not patch around failures and must not pass `--no-verify`.
- **Branch protection**: if the repo requires reviews or status checks, never attempt a merge.
- **Context discipline**: workers return ≤ 200 words. Most tokens belong in the per-worker subagent contexts, not in the orchestrator session.
- **Dirty working tree**: `check-prereqs.sh` exits non-zero on dirty tree. Refuse to start until the user resolves it.

## Output Discipline

- Per-wave updates: 5–10 lines maximum (the PR checklist + the "tell me when merged" line).
- End-of-run summary: 3 lines (count of PRs merged, parent checklist updated, parent close decision pending user).
- No long status reports between waves.
