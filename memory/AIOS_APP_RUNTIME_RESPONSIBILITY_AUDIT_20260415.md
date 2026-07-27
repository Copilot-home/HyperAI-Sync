# AIOS App Runtime Responsibility Audit - 2026-04-15

## Purpose

Map what the current AI server/app runtime is responsible for so the system can harden it without confusing live authority, lineage material, operator cockpit, and downstream economy lanes.

This audit is read-only. It does not mutate OS, Docker, WSL, backend/frontend runtime, economy execution, or archive surfaces.

## Runtime Identity

| Layer | Current measured/canon truth |
| --- | --- |
| Product surface | `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system` |
| Backend authority | `backend/server.js` |
| Backend URL | `http://127.0.0.1:5000` |
| Frontend authority | `src/main.tsx -> src/App.tsx`, served from `dist-isolated` |
| Frontend URL | `http://127.0.0.1:4173` |
| Runtime mode | `default-runtime` |
| Boundary state | `autonomous` |
| Runtime strategy | `default_runtime_active` |
| Managed runtime | not required / missing |
| Operator relay | not required for routine runtime decisions |

## Live Responsibility Map

| Responsibility | Evidence | Current status | Notes |
| --- | --- | --- | --- |
| Health heartbeat | `GET /api/health` | live | Returns `APO-NET Core Active`. |
| Runtime capability declaration | `GET /api/runtime/capabilities` | live | Declares autonomous boundary, core/non-core/degraded lanes, selected action, and runtime authority. |
| Runtime ecosystem scan | `GET /api/runtime/ecosystems`, `GET /api/runtime/ecosystem`, `GET /api/runtime/state` | live/source-backed | Reads ecosystem/runtime state from local artifacts and source truth. |
| Workspace cockpit data | `/api/workspace/session`, `/graph`, `/lanes`, `/runtimes`, `/connectors`, `/missions`, `/proof`, `/providers` | live/source-backed | Serves the app's control-plane view for the UI. |
| Mission intake | `GET/POST /api/workspace/missions`, `GET /api/workspace/missions/:id` | live/source-backed | Accepts local mission records; should remain governed by mission templates and evidence requirements. |
| Chat routing | `POST /api/workspace/chat/route`, `GET/POST /api/chat/messages` | degraded/local-only | Chat is a command/local bridge, not proof of external conversational intelligence or business truth. |
| Autonomy policy | `GET /api/autonomy/policy` | live | Browser-safe authority snapshot for routine runtime action. |
| Autonomy state | `/api/autonomy/status`, `/objectives`, `/executions`, `/probes`, `/decisions`, `/snapshots` | live | Tracks preserve-communication, stabilize-symphony, protect-user-context objectives. |
| Autonomy control | `POST /api/autonomy/start`, `/stop`, `/heartbeat`, `/objectives`, `/tick` | live but sensitive | Mutates local autonomy state; should stay behind mission/evidence/rollback rules for non-routine use. |
| Runtime reconcile | `POST /api/runtime/reconcile` | live but sensitive | Can influence runtime policy; must not be used to bypass root-host/degraded-shell invariants. |
| User/operator profile | `/api/users`, `/api/users/current`, `/api/users/:id` | live stub/profile lane | Supports local operator profile and UI state; not identity authority for GitHub or OS. |
| Empathy lane | `/api/empathy/status`, `/analytics`, `/process` | live non-core | Operational support lane; not shell authority. |
| Vietnamese cultural analysis | `/api/vietnamese/analyze`, `/generate` | live non-core | Used by autonomy ticks and cultural analysis; not external publish authority. |
| NotebookLM lane | `/api/notebooklm/status`, `/notebooks`, `/sources` | degraded stub | Route contract exists, but upstream credentials/production autonomy are not proven. |
| Symphony orchestration | `/api/symphony/status`, `/frequency`, `/start`, `/stop` | live core | Core command/control lane. |
| GitHub-agent surface | `/api/github-agent/status`, `/query` | live/source-declared | Needs identity/auth gate before becoming GitHub authority. |
| WebSocket/realtime telemetry | source/client lineage | frozen/unproven | Not authoritative until explicitly re-proven. |
| TypeScript backend surface | `backend/server.ts` | frozen | Not CI/runtime truth. |

## Core Boundary

The app runtime is currently responsible for these core lanes:

1. `dashboard`
2. `symphony`
3. `runtime`
4. `autonomy`

These are the lanes where the runtime may be treated as the current product shell authority after live proof.

## Non-Core Operational Lanes

The app runtime also serves these lanes, but they must not be promoted to shell authority:

1. `empathy`
2. `vietnamese`
3. `notebooklm`
4. `users`

These are useful support lanes. They may inform UI and autonomy, but they should remain bounded by evidence and mission rules.

## Degraded / Frozen Lanes

| Lane | State | Hard rule |
| --- | --- | --- |
| Chat | degraded/local-only | Do not treat chat output as canonical runtime truth without evidence artifact. |
| NotebookLM | operational stub | Do not treat as production integration until credentials and live upstream proof exist. |
| WebSocket clients | frozen/unproven | Do not use as authority for live telemetry until re-proven. |
| `backend/server.ts` | frozen architecture | Do not treat as backend runtime truth unless backend-unification is explicitly opened. |
| Managed runtime | missing/not required | Do not force managed recovery while default runtime is healthy. |

## What This Runtime Is Responsible For

The runtime is responsible for:

1. keeping the local product shell reachable on `5000/4173`;
2. serving the control dashboard and workspace cockpit;
3. exposing runtime capability and autonomy policy truth;
4. keeping the symphony/autonomy loop observable;
5. preserving communication between backend, browser shell, and local orchestration surfaces;
6. providing bounded non-core support lanes for empathy, Vietnamese analysis, NotebookLM stub, and local user profile;
7. reflecting local ecosystem state from governed artifacts;
8. refusing to turn degraded or downstream lanes into authority without proof.

## What This Runtime Is Not Responsible For

The runtime is not responsible for:

1. OS repair, Windows reset, Docker purge, WSL reset, or root-host destructive recovery;
2. external business execution, Telegram publish, TON wallet action, or marketplace publish;
3. GitHub identity truth without explicit `gh`/git identity verification;
4. proving archive or lineage surfaces are active runtime authority;
5. replacing the local Codex/AIOS operator cockpit;
6. treating browser/chat/session presence as business or system truth.

## Hardening Priorities

| Priority | Action | Reason |
| --- | --- | --- |
| P0 | Keep `backend/server.js` as the single backend runtime truth and keep `ci.yml` as CI truth. | Prevents TypeScript/backend drift and false runtime assumptions. |
| P0 | Add or maintain a machine-readable responsibility matrix for all live routes. | Future agents can see which endpoints are core, non-core, degraded, or frozen. |
| P0 | Gate all mutating autonomy/runtime endpoints with mission + evidence + rollback semantics. | `POST /api/autonomy/*` and `POST /api/runtime/reconcile` are useful but sensitive. |
| P1 | Surface degraded state clearly in UI for chat, NotebookLM, WebSocket, managed runtime. | Reduces creator confusion and prevents overclaim. |
| P1 | Reconcile stale capsule statements with the newer live route map. | Agent 3 capsule still contains older broken-lane language that now conflicts with current probes for some lanes. |
| P1 | Preserve default runtime when healthy; do not force managed runtime recovery. | Current policy says default runtime is healthy and managed runtime is not required. |
| P2 | Define exact promotion criteria for GitHub-agent, NotebookLM, WebSocket, and external execution lanes. | These are useful but should not become authority accidentally. |

## Current Risk

The main risk is not that the app runtime is dead. The measured state says it is alive and autonomous-core-ready.

The main risk is responsibility drift:

1. Some lanes are live but non-core.
2. Some lanes are route-present but stub/degraded.
3. Some older memory capsules still describe earlier broken-lane states.
4. Mutating runtime endpoints exist and need strict governance so they do not bypass root-host invariants.

## Recommended Next Action

Create a machine-readable route responsibility matrix under:

`runtime/federation_orchestrator/app_runtime_responsibility_matrix.json`

Then update `agent2_runtime_entrypoint_capsule.md`, `agent3_api_client_contract_capsule.md`, and `agent6_synthesis_capsule.md` with only the delta:

- current core lanes;
- current non-core live lanes;
- degraded/frozen lanes;
- sensitive mutating endpoints;
- hardening priorities.
