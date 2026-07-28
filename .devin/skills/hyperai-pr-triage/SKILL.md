---
name: hyperai-pr-triage
description: Autonomous GitHub PR triage and bounded-write cleanup for the NguyenCuong1989 / Copilot-home ecosystem. Trigger for any task involving PR triage, open PR cleanup, CI-failure PRs, merge conflicts, stale drafts, review-required PRs, or ecosystem queue hygiene. It embodies the lessons from 2026-07-28 and applies low-risk actions (close/merge/update branch/resolve small conflicts/review/approve) without asking for micro-permission on each PR.
author: andy
tags:
  - github
  - pr
  - triage
  - cleanup
  - ci
  - merge
  - conflict
  - review
  - autonomous
user-invocable: true
disable-model-invocation: false
---

# HyperAI PR Triage

Autonomous, bounded-action PR cleanup for the HyperAI ecosystem.

## Triggers

Use this skill when the user says anything like:

- "triage PRs", "clean up PRs", "merge open PRs", "close stale PRs"
- "fix CI failure PRs", "process PRs", "rà soát PR", "xử lý PR"
- "failure mission", "cleanup PR queue", "giảm open PRs"
- Specific PR numbers, repos, or ecosystems of repos.

## Required information

If not already known, collect:

- Owners to scan (default: `NguyenCuong1989`, `Copilot-home`)
- Stale threshold in days (default: `90`)
- Whether to mutate or dry-run (default: dry-run unless user approves)

## Mission contract

For every run, emit and record:

1. `MISSION_PACKET` — objective, target surface, risk class (`bounded_write`), requested action, approval state.
2. `SKILL_ROUTING_TABLE` — `hyperai-pr-triage` selected; `gh` CLI + `hyperai_pr_triage_agent.py` as tools.
3. `MEMORY_CONTEXT` — `memory/project_state.json`, `memory/pr_triage_method_update_*.md`, latest triage report.
4. `ACTION_PACKET` — classify, then execute low-risk actions.
5. `VERIFY_PACKET` — `gh pr list --state open` count; `gh pr view --json state,mergedAt`; `tools/hyperai_pr_triage_loop.py` final state.
6. `ROLLBACK_PACKET` — `gh pr reopen` for closed PRs; revert PRs for merges.
7. `QUEUE_UPDATE` — next triage pass or manual-review list.

## Disposition rules (apply without asking per PR)

| Category | Rule | Action |
|---|---|---|
| `junk` | title is `hi`, `hello`, `test`, or <4 chars; or file count is huge and unreviewable | close with comment |
| `archived-repo` | `gh repo view --json isArchived` returns `true` | classify as `blocked-archived`; do not keep trying unless user explicitly asks to unarchive |
| `wip-draft-empty` | draft or `[WIP]` title and `files` is empty or test output | close or convert to draft |
| `wip-repo-wide-failures` | large draft with failures caused by pre-existing repo issues (latex package, flake8 over unrelated dirs, missing Python APIs) | close as `not_planned`; ask to split and clean |
| `merge` | non-draft, `CLEAN`, `MERGEABLE`, checks `SUCCESS`, `reviewDecision != REVIEW_REQUIRED` | merge (squash default) |
| `unstable-clean-checks` | `UNSTABLE` / `UNKNOWN` but checks pass, `MERGEABLE` | `gh pr update-branch` then merge |
| `ci-failure-fixable` | failing check is a known, small pattern (YAML syntax, SSH checkout, wrong Docker image, unpinned action, missing file, syntax error) | clone, fix, push, re-run, merge |
| `label-required` | status check `Ensure Required Labels` / `PR labels` fails | add required label if it exists; if repo archived, block |
| `review-required` | `BLOCKED` with `REVIEW_REQUIRED` and all checks pass | approve; resolve review threads via GraphQL if `required_conversation_resolution` is enabled; then merge |
| `agent-review-policy-block` | merge fails with "Approvals from users that collaborated with the coding agent..." | classify as `blocked-agent-review`; do not silently change branch protection; surface to user |
| `small-conflict` | `CONFLICTING` in 1-2 small source files where both sides add distinct entries | merge base into branch, resolve keeping both additions, commit, push, merge |
| `large-conflict` | many workflow files or large refactor conflict | close with comment asking for rebase |

## Tool commands

```bash
# Dry-run scan across default owners
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_agent.py --stale-days 90 --mission-id <id>

# Execute low-risk actions
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_agent.py --stale-days 90 --execute --mission-id <id>

# Autonomous loop until queue is exhausted
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_loop.py --stale-days 90 --max-iter 5 --sleep 15
```

## Heuristics for fixable CI failures

1. **CircleCI YAML parse error** — read `.circleci/config.yml`, fix quoting/heredoc, ensure valid YAML.
2. **CircleCI SSH checkout on private repo** — replace `checkout` with HTTPS clone using `CIRCLE_PROJECT_USERNAME`, `CIRCLE_PROJECT_REPONAME`, `CIRCLE_SHA1`, and `GITHUB_TOKEN`.
3. **Wrong Docker image / .NET vs Python** — switch to `cimg/python:3.11` and `python -m compileall` or `python -m pytest` as appropriate.
4. **Vercel unverified commit** — if the PR code is correct, update branch; merge may still be blocked by Vercel policy.
5. **Missing required labels** — inspect `.github/workflows/pr-labels.yml`; add one of the required labels; if label does not exist and repo not archived, create it.
6. **Governance manifest drift** — run `python3 tools/governance/governance_gate.py generate` on the branch, commit, push.
7. **Workflow action SHA pinning** — replace `@v4` with full commit SHA for `actions/checkout`, `actions/setup-python`, etc.
8. **Required conversation resolution** — query GraphQL `reviewThreads`, call `resolveReviewThread` for addressed threads, then merge.

## Verification

- After each batch: `python3 tools/hyperai_pr_triage_loop.py ...`
- Confirm final open PR count and categories.
- Update `memory/project_state.json`, `memory/next_actions.md`, and `memory/pr_triage_method_update_*.md`.
- Commit and push evidence to `HyperAI-Sync`.

## Output discipline

Use the packet output format from `hyperai-runtime-orchestrator`:

```text
MISSION_PACKET
SKILL_ROUTING_TABLE
MEMORY_CONTEXT
ACTION_PACKET
VERIFY_PACKET
ROLLBACK_PACKET
QUEUE_UPDATE
APPROVAL_GATE
```

Keep per-PR output compact; group and aggregate. Do not print secrets or tokens. Do not ask for permission on every low-risk close/merge; ask only for unarchiving repos, changing branch protection, force-pushing, or merging large draft features with repo-wide CI failures unless the user has set `APPROVAL_GATE=OPEN` / `--autonomous`.

## AGENTS.md / Canon compliance

This skill operates under the `HYPERAI / AIOS CANON RUNTIME OPERATING LAW`:

- `CANON is authority` — when the user asks to "load the operating premise and decide", the assistant still applies the AGENTS.md canon as the operational constraint.
- `No anchor, no validity` — every mutation must leave a receipt (commit, log, branch-protection snapshot).
- `Cleanup without receipt -> invalid` — always record branch protection before/after, archive state transitions, and PR state after action.
- `Cloud/public without gate -> not authorized` — unarchiving a repo or changing branch protection is a public/stateful gate; require an explicit `APPROVAL_GATE`.
- `Do not modify repository security policies ... to work around CI or build failures` — branch protection may only be temporarily relaxed as a last resort, and must be restored immediately after the specific merge, with before/after evidence.

### Approval gates

| Gate | Low-risk actions (no per-PR ask) | High-risk actions (need explicit gate) |
|---|---|---|
| `APPROVAL_GATE: DRY-RUN` | classify, report, dry-run | none |
| `APPROVAL_GATE: EXECUTE` | close junk/empty/stale, merge clean PRs, update branch | — |
| `APPROVAL_GATE: AUTONOMOUS-OVERRIDE` | all of the above | unarchive repo, archive repo, modify branch protection, force-push, resolve unaddressed review threads, merge coding-agent PR by bypassing collaborator review rule |

If a high-risk action is needed and the gate is not open, record it as `blocked` in `manual_review` and surface it to the user rather than silently bypassing policy.
