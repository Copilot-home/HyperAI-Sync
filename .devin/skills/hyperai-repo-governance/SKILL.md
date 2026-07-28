# hyperai-repo-governance

Autonomous repository governance across the `NguyenCuong1989` and `Copilot-home` ecosystems. Extends `hyperai-pr-triage` from pull requests to the full open-item surface: open issues, pull requests, Notion-sync mirrors, stale work, and junk/empty issues.

## When to use

- The user asks for repo governance, ecosystem cleanup, issue triage, Notion-sync reconciliation, or applying the PR triage method to the entire repository.
- After `hyperai-pr-triage` reports 0 open PRs and the next surface is open issues.
- When the user says "no ask", "human in the loop = fail", or "apply to whole repo".

## Approval gates

This skill uses the same gates as `hyperai-pr-triage`:

- `DRY-RUN`: classify and report only.
- `EXECUTE`: close junk/stale issues and completed Notion-sync issues.
- `AUTONOMOUS-OVERRIDE`: required when the user explicitly disables human-in-the-loop or authorizes broad governance; log to `security_operations_receipt.json` and restore all branch-protection mutations immediately.

## Workflow

1. **Inventory**: list all repositories under the configured owners.
2. **Collect open items**: fetch open issues and PRs with `gh search issues` and `gh search prs`.
3. **Notion reconciliation**:
   - Extract `Notion Page ID` from `notion-sync` issues.
   - Query the Notion `DB_TASKS` data source via the `notion-mcp-server` `notion-query-data-sources` tool.
   - Build a `(page_id -> Status)` map.
4. **Classify issues**:
   - `notion_done`: Notion status is `Done` -> close as completed.
   - `notion_in_progress`: status is `In Progress` -> keep open.
   - `notion_open`: status is `To-do` -> keep open.
   - `notion_missing`: Notion page not found in DB -> close as stale/missing.
   - `notion_unverified`: issue has `notion-sync` label but no page id -> manual review.
   - `junk`: empty title/body or test/draft title -> close.
   - `stale`: no update for `> stale_days` and no comments -> close.
   - `manual_review`: everything else.
5. **Classify PRs**: reuse `hyperai_pr_triage_agent` logic.
6. **Execute low-risk actions**: close issues with a standardized comment and Devin attribution.
7. **Verify**: re-run `gh search issues` and compare before/after.
8. **Record evidence**: write `governance_report.json` and `governance_executed_summary.json` under `runtime/federation_orchestrator/agent_task_outputs/<mission-id>/`.

## Commands

```bash
cd /Users/andy/HyperAI-Sync

# Dry-run scan
python3 tools/hyperai_repo_governance_agent.py \
  --owners NguyenCuong1989 Copilot-home \
  --notion-status-file <notion-status-json> \
  --stale-days 90 \
  --mission-id mission-repo-governance-YYYYMMDD

# Execute low-risk closures (requires AUTONOMOUS-OVERRIDE if no human confirmation)
python3 tools/hyperai_repo_governance_agent.py \
  --owners NguyenCuong1989 Copilot-home \
  --notion-status-file <notion-status-json> \
  --stale-days 90 \
  --execute \
  --mission-id mission-repo-governance-YYYYMMDD

# Re-run to verify final state
python3 tools/hyperai_repo_governance_agent.py \
  --owners NguyenCuong1989 Copilot-home \
  --notion-status-file <notion-status-json> \
  --stale-days 90 \
  --mission-id mission-repo-governance-YYYYMMDD
```

## Notion status file

The status file is the JSON output of `notion-query-data-sources` against the `DB_TASKS` collection. It must contain objects with `url`, `Task Name`, and `Status` fields:

```json
{
  "results": [
    {"url": "https://app.notion.com/<page-id>", "Task Name": "...", "Status": "Done"}
  ]
}
```

If `notion-status-file` is not provided, Notion-sync issues are classified as `notion_unverified` and left for manual review.

## Output discipline

- Always produce `governance_report.json`.
- After `--execute`, also produce `governance_executed_summary.json` with before/after counts and the list of closed issues.
- Update `memory/project_state.json`, `memory/next_actions.md`, and `runtime/federation_orchestrator/agent_task_outputs/<mission-id>/security_operations_receipt.json`.
- Commit and push evidence to `HyperAI-Sync` when the user says "no ask".

## Safety

- Do not close issues that are `notion_open`, `notion_in_progress`, or `manual_review` without explicit creator override.
- Do not delete repositories, branches, or releases.
- Never log `NOTION_API_KEY` or other secrets.
- If a close operation fails, record the failure and continue; do not retry blindly.
