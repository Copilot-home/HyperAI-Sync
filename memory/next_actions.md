# Next Actions

- [x] Begin key hygiene policy (R5) guardrail for 7 keys without expiry and 1 unused service account key.
- [x] Revoke exposed GitHub PAT (`github_pat_11BO5...`) recorded in `runtime/federation_orchestrator/titan_repo_sync_registry_20260415.json` history. HyperAI mission `mission-c6887acbe9774885` completed; GitHub returned HTTP 202.
- [x] Wire guardrail into `/runtime/actions` execute path and record evidence receipt on policy events.

## Deferred — requires creator gate / external surface

- [ ] Collect manual/dashboard evidence for Domains/SSO/AAC/External Invites/Usage limits/Agents.
- [ ] Generate a replacement GitHub PAT if the revoked token was still in use for any connector.
