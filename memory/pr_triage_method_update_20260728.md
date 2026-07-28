# PR Triage Method Update — 2026-07-28

> Lessons from processing the remaining 11 PRs after the failure mission.

## What changed

- Open PRs dropped from **11 → 2**.
- Closed 5 PRs, merged 6, resolved 1 small conflict manually.
- 2 PRs remain blocked by repo policy / state, not code:
  - `NguyenCuong1989/vscode-python-environments#1` — repository is archived.
  - `Copilot-home/balancehub-minimal#3` — GitHub blocks merge because the PR author is a coding-agent app and the reviewer (NguyenCuong1989) has pushed commits to the same branch, so the approval is disallowed by the current branch protection rule.

## New classification rules to add

1. **Archived repository**
   - Detect `isArchived=true` on the repo.
   - Action: classify as `blocked-archived`; do not spend time on checks. If the mission explicitly requires cleanup, unarchive, close/merge, then re-archive in the same operation window.

2. **Branch protection / review collaboration block**
   - When `mergeStateStatus=BLOCKED` and the error message mentions "Approvals from users that collaborated with the coding agent on changes will not satisfy review requirements", the PR cannot be merged by the current operator identity.
   - Action: `blocked-agent-review-policy`. Options:
     - Find a second reviewer account.
     - Temporarily adjust `required_approving_review_count` / collaborator rule (requires explicit gate; do not silently disable).
     - Surface to the user as a policy decision.

3. **Missing required labels**
   - Some repos (e.g., `vscode-python-environments`) have a workflow that fails unless one of a fixed label set is present.
   - Action: `label-required`. If the label exists, add it and re-run. If the repo is not archived, this often clears `mergeStateStatus=BLOCKED`.

4. **Conversation resolution before merge**
   - `required_conversation_resolution` on `main` means unresolved review threads block merge even with `mergeable=MERGEABLE`.
   - Action: query GraphQL for `reviewThreads{isResolved}` and use `resolveReviewThread` for threads that are already addressed.

5. **Draft/WIP PR with no changed files**
   - If `files` is empty and the title starts with `[WIP]` or the PR is a draft, it is safe to close after a short comment.

6. **Draft with broad, repo-wide CI failures**
   - If a draft PR introduces or touches files that make `flake8`, `pytest`, or `validate` fail because the repo already has non-CI files that violate the linter, the cost to fix exceeds the value of the draft.
   - Action: close as `not_planned` with a note to split and clean.

7. **Self-contained checkout pattern**
   - Repos with an Actions allow-list may not use `actions/checkout`. The canonical fallback is:
     ```bash
     git init -q .
     git remote add origin "https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
     git fetch -q --depth 1 origin "${GITHUB_REF}"
     git checkout -q FETCH_HEAD
     ```
   - This pattern should be recognized and not flagged as an error by the triage agent.

8. **Conflict resolution heuristics for small conflicts**
   - When a conflict is in a single small source file (not a workflow matrix), the agent may attempt an automatic merge keeping both branch additions.
   - When a conflict is in multiple workflow files with large diffs, prefer close / ask for rebase.

9. **Re-approve after branch update**
   - `dismiss_stale_reviews=true` means any new commit invalidates prior approvals.
   - The agent must re-`gh pr review --approve` after `gh pr update-branch` or after pushing a conflict-resolution commit.

10. **Verify after destructive close on archived repo**
    - `gh pr close` on an archived repo fails with a locked-comment error. Use `gh repo unarchive`, close, then `gh repo archive` if mission explicitly requires it.

## Operator checklist for the next run

- [ ] Run `gh repo view <repo> --json isArchived` for unknown repos.
- [ ] Before merging a PR with review required, run `gh pr view --json reviews,reviewDecision`.
- [ ] Before merging a PR after a branch update, re-approve and re-check status.
- [ ] For `mergeStateStatus=BLOCKED`, query branch protection and review threads.
- [ ] For `BLOCKED` with a failing `PR labels` / `Ensure Required Labels` check, inspect the workflow and add a required label.
- [ ] Keep evidence in `runtime/federation_orchestrator/agent_task_outputs/<mission>/`.

## Evidence

- `runtime/federation_orchestrator/agent_task_outputs/mission-pr-triage-loop-20260728v4/`
- `runtime/federation_orchestrator/agent_task_outputs/mission-ci-failure-fix-20260728/`
