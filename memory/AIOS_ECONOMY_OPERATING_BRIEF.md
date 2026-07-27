# AIOS Economy Operating Brief

Date: 2026-04-15

## Operating Boundary

The economy system is a governed first-dollar pipeline, not a free-running automation surface.

Current root constraint:

- Windows root host is conservation-critical.
- `shell_authority` is degraded.
- Docker/WSL/HCS are unavailable for expansion.
- Economy execution is paused until runtime proof is stable.

## Canonical Revenue Rule

Revenue state follows:

`event -> evidence -> ledger -> metric`

Implications:

- No revenue metric without a ledger-backed event.
- No publish confirmation without creator-confirmed evidence.
- No funding confirmation without receive evidence.
- Creator acknowledgement confirms a fact, not business truth.
- Telegram and TON do not become shell authority.

## Current First-Dollar State

| Field | Value |
| --- | --- |
| objective state | `awaiting_publish_evidence` |
| next valid operator action | `publish_confirm` |
| first dollar achieved | `false` |
| artifact ready count | `1` |
| publish relay ready count | `1` |
| published count | `0` |
| funding pending count | `1` |
| funding confirmed count | `0` |
| active publish event | `publish-20260403004302` |
| active funding event | `funding-pending-uber-egift-20260403004325` |
| protected artifact | `runtime/deal_value_engine/artifacts/drafts/uber-egift.md` |

## Workflow

The current economy lane uses this path:

1. Source ingest.
2. Candidate normalize.
3. Deal filter.
4. Deal rank.
5. Creator review.
6. Deal format.
7. Artifact publish-ready.
8. Telegram relay or manual creator relay.
9. Signal capture.
10. Funding pending.
11. Funding confirmed.
12. Ledger-backed first-dollar metric.

## Authority Boundaries

| Surface | Allowed role | Not allowed |
| --- | --- | --- |
| `deal_intelligence` | filter, rank, format under orchestration | shell authority, ledger authority |
| `provider_reasoning` | bounded reasoning and formatting | mission root, evidence recorder |
| `telegram_relay` | publish relay/manual relay support | business truth, shell authority |
| `telegram_execution_fabric` | publish proof execution adapter when shell is stable | mission root |
| `treasury_control` | receive-only balance/funding evidence | spending, custody, approval intake |
| Creator approval surfaces | acknowledge facts and approve relay steps | fabricate publish or funding state |
| `shell_authority` | runtime mutation and execution gate | bypass conservation rules |

## Stop Rules

Stop economy execution when:

- `shell_authority` is degraded.
- root host conservation warning is active.
- Telegram target proof is missing.
- funding evidence is missing.
- verification truth cannot gate the route.
- any lane attempts to create revenue metric before ledger evidence.

Allowed while stopped:

- preserve first-dollar event IDs
- consolidate docs
- scan/read current artifacts
- prepare creator approval language
- update memory with current blockers and next safe action

## Resume Conditions

Economy execution may resume only when:

- root host remains conserved
- shell/runtime proof is stable enough for low-cost probes
- the requested action binds to `telegram_publish_proof` or `funding_reconciliation`
- degradation policy no longer stops the route
- creator approval/fact acknowledgement is captured for the specific event
- evidence recorder is unambiguous

## Next Safe Action

Current safe action is not autoposting or wallet automation. It is preservation:

- keep `publish-20260403004302`
- keep `funding-pending-uber-egift-20260403004325`
- keep `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`
- wait for runtime proof before publish/funding confirmation

