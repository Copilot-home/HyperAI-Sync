# AIOS G(t) Reduction Sprint Plan

Date: 2026-04-15

## Purpose

This plan lowers ecosystem noise `G(t)` without trading away core stability `T`, workflow proof `W`, or formal control `F`.

Sprint 1 is governance-only. It does not mutate OS, Docker, WSL, app code, backend, frontend, Telegram publish state, TON funding state, or archive authority.

## Audit Model

Required model:

```text
H(t) = T + G(t)
dH/dt < 0
lim_t->infinity H(t) = T
D = T x (W + F) - alpha G(t) - beta Th
Trust(S) = T(W + F)/(1 + G(t)) + Th
```

Baseline variables:

| Variable | Value | Meaning |
| --- | ---: | --- |
| `T` | `0.78` | Core authority and conservation stability |
| `G(t)` | `0.34` | Current ecosystem noise and ambiguity |
| `Th` | `0.62` | Defensive threshold and friction |
| `W` | `0.72` | Workflow proof strength |
| `F` | `0.68` | Formal control-plane strength |
| `alpha` | `0.70` | Noise penalty coefficient |
| `beta` | `0.30` | Threshold/friction penalty coefficient |

Baseline calculations:

```text
H(t) = 0.78 + 0.34 = 1.12
D = 0.78 x (0.72 + 0.68) - 0.70 x 0.34 - 0.30 x 0.62 = 0.668
Trust(S) = 0.78(0.72 + 0.68)/(1 + 0.34) + 0.62 = 1.435
```

## Sprint Targets

| Sprint | Target `G(t)` | Reduction mechanism | Runtime mutation |
| --- | ---: | --- | --- |
| Sprint 1 | `0.28` | classify surfaces, lock stop rules, write root-host checklist | no |
| Sprint 2 | `0.22` | prove minimal runtime path or keep blocked cleanly with rollback | only after explicit proof plan |
| Sprint 3 | `0.16` | economy resume gate or clean continued block | only if gate permits |

Sprint 1 expected calculations:

```text
H(t) = 0.78 + 0.28 = 1.06
D = 0.78 x (0.72 + 0.68) - 0.70 x 0.28 - 0.30 x 0.62 = 0.710
Trust(S) = 0.78(0.72 + 0.68)/(1 + 0.28) + 0.62 = 1.473
```

## Sprint 1 Scope

Allowed:

- document consolidation
- memory planning
- machine-readable trace artifact
- root-host deployment checklist
- capsule ownership updates
- readiness review
- low-cost artifact inspection

Blocked:

- OS reset
- Docker purge or reset
- WSL reset
- root runtime deletion
- app code change
- backend/frontend behavior change
- Telegram publish confirmation
- TON or treasury funding confirmation
- archive promotion

## Sprint 1 Acceptance

- `memory/AIOS_ROOT_HOST_DEPLOYMENT_CHECKLIST.md` exists and blocks destructive root-host actions while shell/root host are degraded.
- `runtime/federation_orchestrator/g_reduction_trace.json` exists and preserves baseline variables plus first-dollar state.
- First-dollar state remains unchanged:
  - `publish-20260403004302`
  - `funding-pending-uber-egift-20260403004325`
  - `runtime/deal_value_engine/artifacts/drafts/uber-egift.md`
- No app code changes are required.
- No `npm run ci:build` or `npm run ci:browser-smoke` is required.

## Next Sprint Gate

Sprint 2 cannot start runtime-impacting work until a rollback plan exists and the action binds to a mission template.

