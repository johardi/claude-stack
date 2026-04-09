---
name: review-issue
description: Summarize and triage ontology repo issues for contribution. Use whenever the user wants to review an issue, find good first issues, summarize open issues for an ontology, or understand what an NTR or other issue needs—e.g. "review this issue", "is this a good first issue", "summarize open issues for this ontology", "what does this NTR need". Use for both single-issue review and listing/batching issues.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, WebFetch, WebSearch]
---

# Review Issue Skill

Use this skill when the user wants to **understand one or more issues** in an ontology repository—for example to pick work, assess difficulty, or see what a new term request (NTR) or other issue requires. You summarize issue type, required fields (vs any template), labels, and suitability for a first contribution or agent-driven change.

## When to Use

- User asks to **review an issue** (by number or URL) or **"is this a good first issue"**.
- User wants to **summarize open issues** for a repo (e.g. list by type, filter by label).
- User asks **"what does this NTR need"** or what to provide for a synonym/obsoletion/term-merge issue.
- After **analyze-project** or **clone-project**: to choose which issue to implement before making edits.

Use **web fetch** (GitHub issue/API pages) or, if the repo is cloned under `projects/<slug>/`, you can combine with reading CONTRIBUTING/issue templates from disk.

## Workflow

1. **Identify repo and issue(s)**: From the user's message, get the repo (owner/name or URL) and either a single issue number (or URL) or a request to list/filter issues (e.g. open, with label "good first issue" or "New term request").
2. **Fetch issue data**: For each issue, obtain title, body, labels, and if possible the issue template used (from `.github/ISSUE_TEMPLATE/` or from the issue form). Use the GitHub web interface or API (e.g. fetch issue page, list issues).
3. **Classify**: For each issue, determine:
   - **Type**: e.g. new term request (NTR), synonym, definition, obsoletion, term merge, missing parent/superclass, bug, documentation, refactoring, mapping.
   - **Labels**: workflow/type labels (NTR, bug, help wanted, good first issue) and any domain/project labels.
   - **Required fields**: From the issue template or CONTRIBUTING, what the maintainers expect (e.g. label, definition, parent, PMIDs, hierarchy position, replace_by/consider for obsoletion).
   - **Suitability**: Whether it looks like a good first contribution, or agent-friendly (well-scoped, template-driven), or needs more discussion/clarification.
4. **Summarize**: Produce a short review (see Output format).

## Output Format

For **one issue**:

- **Issue**: #N – title.
- **Type**: e.g. NTR, synonym, obsoletion, bug.
- **Labels**: list relevant labels.
- **Required / expected**: What the template or CONTRIBUTING says to provide (e.g. definition, parent, refs).
- **Suitability**: Good first issue? Agent-friendly? Needs more info?

For **multiple issues** (list/summary):

- **Repo**: owner/repo (or slug).
- **Issues**: Table or list with issue number, title, type, key labels, one-line summary; optionally mark "good first" or "NTR with template".
- **Suggested next step**: e.g. "Implement #N (NTR with clear template)" or "Clarify #M with maintainers."

## Notes

- If CONTRIBUTING or issue templates were captured in **analyze-project**, reuse that to interpret what "required" means for NTRs or other types.
- This skill does not implement the issue; it only reviews and summarizes. Implementation is done in the project directory using ontology-editor and ODK skills, then **create-pull-request** for branch and PR.
