# Next Actions

- [x] Begin key hygiene policy (R5) guardrail for 7 keys without expiry and 1 unused service account key.
- [x] Revoke exposed GitHub PAT (`github_pat_11BO5...`) recorded in `runtime/federation_orchestrator/titan_repo_sync_registry_20260415.json` history. HyperAI mission `mission-c6887acbe9774885` completed; GitHub returned HTTP 202.
- [x] Wire guardrail into `/runtime/actions` execute path and record evidence receipt on policy events.
- [x] Collect manual/dashboard evidence for Domains/SSO/AAC/External Invites/Usage limits/Agents (mission-d785a4e3a4ab47d1; evidence via Playwright probe + authenticated gh REST/GraphQL).
- [x] Materialize HyperAI Runtime Orchestrator skill: canonical at `/Users/andy/.agents/skills/hyperai-runtime-orchestrator/SKILL.md`, symlinked from `~/.config/devin/skills/hyperai-runtime-orchestrator`.
- [x] Audit all open issues/PRs across NguyenCuong1989 and Copilot-home (mission-8fd3a8d531744837). Closed 5 stale/vague issues and 9 stale/draft/junk PRs. Evidence at `runtime/federation_orchestrator/agent_task_outputs/mission-ecosystem-audit-20260728`.
- [x] Build reusable PR triage agent `tools/hyperai_pr_triage_agent.py`.
- [x] Build and run HyperAI PR triage autonomous loop `tools/hyperai_pr_triage_loop.py`. Loop completed after 1 iteration (21 PRs, 0 low-risk actions). Evidence at `runtime/federation_orchestrator/agent_task_outputs/mission-pr-triage-loop-20260728`.
- [x] **Failure mission:** cleared all 9 CI-failure PRs plus `Copilot-home/nguyencuong_2509#3`. Merged 10, closed 1 (`my_too_test#9`), and re-ran triage loop; open PR count reduced from 21 to 11. Evidence at `runtime/federation_orchestrator/agent_task_outputs/mission-pr-triage-loop-20260728v3`.
- [x] **Cleanup phase 2:** processed the remaining 11 PRs (5 closed, 6 merged, 1 small conflict resolved). Open PRs now 0. Method and skill updated. Evidence at `runtime/federation_orchestrator/agent_task_outputs/mission-pr-cleanup-phase2-20260728` and `mission-pr-triage-loop-20260728v5`.
- [x] **Skill upgrade:** created `hyperai-pr-triage` skill in `.devin/skills/hyperai-pr-triage/SKILL.md`, upgraded `tools/hyperai_pr_triage_agent.py` with archive/label/conflict heuristics, and added AGENTS.md/Canon approval-gate guardrails for high-risk operations.

## Reusable PR triage agent & loop

```bash
# Dry-run scan across default owners
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_agent.py --stale-days 90 --mission-id <mission-id>

# Execute low-risk actions
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_agent.py --stale-days 90 --execute --mission-id <mission-id>

# Autonomous loop (runs until no low-risk actions)
cd /Users/andy/HyperAI-Sync
python3 tools/hyperai_pr_triage_loop.py --stale-days 90 --max-iter 5 --sleep 15
```

## Creator gate (one-click / policy)

- [ ] Generate replacement GitHub PAT by opening the pre-filled URL after logging in, then store it in the APΩ credential broker.
  - Pre-filled URL: `https://github.com/settings/personal-access-tokens/new?name=HyperAI-replacement-PAT&description=Replacement+for+revoked+exposed+token&target_name=Copilot-home&expires_in=90&contents=read&metadata=read&actions=read`
- [ ] Verify domains `creators.contact` and `example.com` if they should be marked verified.
- [ ] Assess SAML/AAC setup if enterprise requirements change.

## Ecosystem cleanup

- [x] Open PRs: 0 across NguyenCuong1989 and Copilot-home.
- [ ] Triage 85 Notion-sync issues in `NguyenCuong1989/trust_of_copilot-c8aae4ab` against Notion source.
- [ ] Decide disposition of 6 old DAIOF principle issues in `Copilot-home/DAIOF-Framework` (#27-37, #78).
- [ ] Assess balancehub-minimal `ops/secret_hygiene.py` Codex review feedback (P1/P2) for a follow-up cleanup PR.

## Method & skill documentation

- `memory/pr_triage_method_update_20260728.md` — 10 lessons from the cleanup.
- `.devin/skills/hyperai-pr-triage/SKILL.md` — autonomous skill for PR triage with Canon approval gates.
- `tools/hyperai_pr_triage_agent.py` — agent with archive/label/conflict heuristics.
