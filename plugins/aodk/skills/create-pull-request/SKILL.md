---
name: create-pull-request
description: Create a branch, commit, push, and open a pull request from the current project directory. Use whenever the user wants to create a PR for their changes, open a pull request for an issue, or draft a PR description—e.g. "create a PR for this change", "open a pull request for issue #N", "draft a PR description". Assumes the agent is already in the clone root (e.g. projects/<name>/).
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash]
---

# Create Pull Request Skill

Use this skill when the user wants to **create a pull request** for changes made in a cloned ontology project. You work **from the project directory** (e.g. `projects/<slug>/`): create a branch, commit, push, then open a PR with a description that matches the project's norms (summary, "Closes #N", optional change table and checklist). If GitHub CLI (`gh`) is available, use it to create the PR; otherwise provide the exact commands and a ready-to-paste PR body.

## When to Use

- User says **"create a PR for this change"**, **"open a pull request for issue #N"**, **"draft a PR description"**, or similar.
- After implementing an issue in a clone: changes are in `projects/<slug>/`; the agent has already cd'd into that directory. This skill handles branch, commit, push, and PR creation from there.

**Assumption**: The current working directory is the **clone root** (e.g. `projects/owner-repo/`). All Git commands (branch, commit, push) and any `gh` calls run from that directory. If the user is not in the clone root, remind them to cd into the project directory first (or do it as part of the workflow).

## Workflow

1. **Confirm context**: Ensure you are in the clone root (e.g. `projects/<slug>/`). If not, change directory there before running Git or `gh` commands.
2. **Branch**: Create a branch name that matches the project's conventions (often `issue-<N>` or `feature/<term-name>`). Run `git checkout -b <branch-name>`.
3. **Commit**: Stage the relevant files and commit with a clear message (e.g. "Add term X (Closes #N)" or "Fix synonym for Y"). Run `git add` and `git commit`.
4. **Push**: Push the branch to the user's fork or the same repo: `git push -u origin <branch-name>`. If the clone points to upstream, the user may need a fork and a remote named `origin`; document that if needed.
5. **PR description**: Compose a PR body that fits the project's expectations (from **analyze-project** or CONTRIBUTING):
   - **Summary**: One line and "Closes #N" (or "Fixes #N").
   - **Changes**: Optional table (term added, obsoletion, etc.) or bullet list.
   - **Rationale**: Brief justification if the project uses it.
   - **Checklist**: If the project expects one, include and mark items.
6. **Open the PR**: If **GitHub CLI** (`gh`) is available and authenticated, run e.g. `gh pr create --title "..." --body "..."` from the clone root. Otherwise, output the PR title and body for the user to paste into the GitHub form.

## Branch Naming

- Prefer patterns observed in the repo (e.g. `issue-123`, `feature/term-label`, `fix/synonym-xyz`). If unknown, use `issue-<N>` when closing an issue, or `feature/<short-description>`.

## PR Body Conventions

Many ontology repos expect:

- **Link to issue**: "Closes #N" or "Fixes #N" in the description.
- **Structured change**: For term additions/obsoletions, a small table (term ID, label, definition, parent, etc.) or a bullet list of changes.
- **Checklist**: Items such as: plan reviewed, pre-validation done, term search done, edits done, automated validation passed. Align with the project's PULL_REQUEST_TEMPLATE or CONTRIBUTING.

## GitHub CLI

- If `gh pr create` is available, use it so the user gets a single command flow. If not, provide the full PR title and body and the URL to open a PR (e.g. `https://github.com/owner/repo/compare/main...<branch>`).
- If the user has not configured a fork or `origin`, explain that they may need to add a remote and push to their fork, then open the PR from the fork to the upstream repo.

## Output

- Confirm branch name, commit message, and that push succeeded.
- Either: link to the new PR (from `gh pr create` output) or the PR title + body + URL for the user to open the PR manually.
