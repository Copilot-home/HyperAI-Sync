# AIOS Root Host Deployment Checklist

Date: 2026-04-15

## Purpose

This checklist is the required gate before any action that touches the root host, runtime authority, economy execution, ledger evidence, or ecosystem promotion.

The Windows machine is the root host. Preserve it first.

## Preflight

- [ ] Read `memory/AIOS_INVARIANTS.md`.
- [ ] If the action originates from VS Code or an extension, read `memory/AIOS_VSCODE_EXTENSION_DEGRADED_SHELL_POLICY.md`.
- [ ] Read `memory/AIOS_ECOSYSTEM_SYNC_CANON.md`.
- [ ] Read `runtime/federation_orchestrator/ecosystem_sync_readiness.json`.
- [ ] Read `memory/AIOS_RUNTIME_CLASS_MATRIX_20260415.md`.
- [ ] Read `memory/AIOS_ECONOMY_OPERATING_BRIEF.md`.
- [ ] Bind the requested work to exactly one mission template.
- [ ] Confirm the action does not violate any invariant in `memory/AIOS_INVARIANTS.md`.
- [ ] If `shell_authority=degraded`, classify VS Code/extension commands as `allowed`, `approval_required`, or `blocked`.
- [ ] Classify the action as one of: read-only, memory-only, runtime probe, app code change, economy execution, ledger evidence, archive review, destructive operation.

## Immediate Reject Conditions

Reject the action if any condition is true while root host or shell authority is degraded:

- [ ] OS reset or reinstall.
- [ ] Docker purge, Docker factory reset, or Docker data deletion.
- [ ] WSL reset, distro deletion, or HCS destructive repair.
- [ ] Root runtime deletion.
- [ ] Economy execution without readiness gate approval.
- [ ] Telegram publish confirmation without creator-confirmed evidence.
- [ ] TON/funding confirmation without receive evidence.
- [ ] Archive or lineage promotion without proof artifact and rollback path.
- [ ] Browser/editor/creator surface attempts to become shell authority.
- [ ] Provider reasoning attempts to become mission root, shell authority, or evidence recorder.

## Required Before Runtime Probe

- [ ] Define the exact evidence artifact path.
- [ ] Define rollback plan.
- [ ] Confirm the probe does not require Docker/WSL reset.
- [ ] Confirm the probe does not delete or overwrite runtime state.
- [ ] Confirm the probe respects `backend/server.js` as backend runtime truth and `.github/workflows/ci.yml` as CI truth.
- [ ] Confirm whether build/smoke is required by repo verification rules.

## Required Before Economy Action

- [ ] Confirm `economy_execution_allowed` is true in readiness.
- [ ] Confirm shell/runtime proof is stable.
- [ ] Confirm the mission template is `telegram_publish_proof` or `funding_reconciliation`.
- [ ] Confirm the active publish event remains `publish-20260403004302`.
- [ ] Confirm the active funding event remains `funding-pending-uber-egift-20260403004325`.
- [ ] Confirm the protected artifact remains `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`.
- [ ] Confirm creator acknowledgement is event-specific.
- [ ] Confirm the evidence recorder is unambiguous.

## Post-Action Requirements

- [ ] Write or verify the proof artifact.
- [ ] Update memory through `python tools/update_memory.py`.
- [ ] Recalculate `H(t)=T+G(t)`.
- [ ] Recalculate `D=T x (W+F) - alpha G(t) - beta Th`.
- [ ] Recalculate `Trust(S)=T(W+F)/(1+G(t))+Th`.
- [ ] Re-audit `T`, `G(t)`, `Th`, `W`, `F`, `D`, and `Trust(S)` after any major shell, economy, or root-host status change.
- [ ] Record verified, not verified, blocker, and next action.
