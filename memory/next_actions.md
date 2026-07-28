# Next Actions

- [x] Begin key hygiene policy (R5) guardrail for 7 keys without expiry and 1 unused service account key.
- [x] Revoke exposed GitHub PAT (`github_pat_11BO5...`) recorded in `runtime/federation_orchestrator/titan_repo_sync_registry_20260415.json` history. HyperAI mission `mission-c6887acbe9774885` completed; GitHub returned HTTP 202.
- [x] Wire guardrail into `/runtime/actions` execute path and record evidence receipt on policy events.
- [x] Collect manual/dashboard evidence for Domains/SSO/AAC/External Invites/Usage limits/Agents (mission-d785a4e3a4ab47d1; evidence via Playwright probe + authenticated gh REST/GraphQL).

## Creator gate (one-click / policy)

- [ ] Generate replacement GitHub PAT by opening the pre-filled URL after logging in, then store it in the APΩ credential broker.
  - Pre-filled URL: `https://github.com/settings/personal-access-tokens/new?name=HyperAI-replacement-PAT&description=Replacement+for+revoked+exposed+token&target_name=Copilot-home&expires_in=90&contents=read&metadata=read&actions=read`
- [ ] Verify domains `creators.contact` and `example.com` if they should be marked verified.
- [ ] Assess SAML/AAC setup if enterprise requirements change.
