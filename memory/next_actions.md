# Next Actions

- [x] Begin key hygiene policy (R5) guardrail for 7 keys without expiry and 1 unused service account key.
- [x] Revoke exposed GitHub PAT (`github_pat_11BO5...`) recorded in `runtime/federation_orchestrator/titan_repo_sync_registry_20260415.json` history. HyperAI mission `mission-c6887acbe9774885` completed; GitHub returned HTTP 202.
- [x] Wire guardrail into `/runtime/actions` execute path and record evidence receipt on policy events.
- [x] Collect manual/dashboard evidence for Domains/SSO/AAC/External Invites/Usage limits/Agents (mission-d785a4e3a4ab47d1; evidence via Playwright probe + authenticated gh REST/GraphQL).
- [x] Materialize HyperAI Runtime Orchestrator skill: canonical at `/Users/andy/.agents/skills/hyperai-runtime-orchestrator/SKILL.md`, symlinked from `~/.config/devin/skills/hyperai-runtime-orchestrator`.
- [x] Audit all open issues/PRs across NguyenCuong1989 and Copilot-home (mission-8fd3a8d531744837). Closed 5 stale/vague issues and 9 stale/draft/junk PRs. Evidence at `runtime/federation_orchestrator/agent_task_outputs/mission-ecosystem-audit-20260728`.
- [x] Build reusable PR triage agent `tools/hyperai_pr_triage_agent.py` and run it on remaining 22 PRs; closed 1 stale WIP (`NguyenCuong1989/trust_of_copilot-c8aae4ab#30`). 21 PRs remain for manual review.

## Reusable PR triage agent

```bash
# dry-run
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_agent.py --stale-days 90 --mission-id <mission-id>

# execute low-risk close/merge
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_agent.py --stale-days 90 --execute --mission-id <mission-id>
```

## Creator gate (one-click / policy)

- [ ] Generate replacement GitHub PAT by opening the pre-filled URL after logging in, then store it in the APΩ credential broker.
  - Pre-filled URL: `https://github.com/settings/personal-access-tokens/new?name=HyperAI-replacement-PAT&description=Replacement+for+revoked+exposed+token&target_name=Copilot-home&expires_in=90&contents=read&metadata=read&actions=read`
- [ ] Verify domains `creators.contact` and `example.com` if they should be marked verified.
- [ ] Assess SAML/AAC setup if enterprise requirements change.

## Ecosystem cleanup manual review

- [ ] Review 21 remaining open PRs in `runtime/federation_orchestrator/agent_task_outputs/mission-pr-triage-20260728/triage_report.json`; decide merge/close/fix per repo.
- [ ] Triage 85 Notion-sync issues in `NguyenCuong1989/trust_of_copilot-c8aae4ab` against Notion source.
- [ ] Decide disposition of 6 old DAIOF principle issues in `Copilot-home/DAIOF-Framework` (#27-37, #78).
