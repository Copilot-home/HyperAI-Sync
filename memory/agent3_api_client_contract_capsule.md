# Agent 3 API/Client Contract Capsule

## Scope

- Product surface: `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`
- Runtime truth used: live process truth constrained to the currently active `backend/server.js` process on port `5000`
- Proven live endpoints only:
  - `GET /api/health`
  - `GET /api/symphony/status`
  - `POST /api/symphony/start`
  - `POST /api/symphony/stop`

## Client To Endpoint Mapping

- `chatAPI.receiveMessages` -> `GET /api/chat/messages` -> fallback-only
- `chatAPI.sendMessage` -> `POST /api/chat/messages` -> fallback-only

- `empathyAPI.processEmpathy` -> `POST /api/empathy/process` -> broken by live runtime
- `empathyAPI.getSymphonyStatus` -> `GET /api/empathy/status` -> broken by live runtime
- `empathyAPI.getEmpathyScore` -> `GET /api/empathy/status` -> broken by live runtime
- `empathyAPI.subscribeToEmpathyUpdates` -> polling `GET /api/empathy/status` -> broken by live runtime
- `empathyAPI.fetchAnalyticsData` -> `GET /api/empathy/analytics` -> broken by live runtime

- `notebooklmAPI.getNotebookLMStatus` -> `GET /api/notebooklm/status` -> declared but unproven in source, broken by current live runtime
- `notebooklmAPI.listNotebookLMNotebooks` -> `GET /api/notebooklm/notebooks` -> declared but unproven in source, broken by current live runtime
- `notebooklmAPI.createNotebookLMNotebook` -> `POST /api/notebooklm/notebooks` -> declared but unproven in source, broken by current live runtime
- `notebooklmAPI.addNotebookLMSource` -> `POST /api/notebooklm/notebooks/:notebookId/sources` -> declared but unproven in source, broken by current live runtime

- `symphonyAPI.getSymphonyStatus` -> `GET /api/symphony/status` -> declared but unproven helper, endpoint live
- `symphonyAPI.getSymphonyMetrics` -> `GET /api/symphony/status` -> live-aligned
- `symphonyAPI.startSymphony` -> `POST /api/symphony/start` -> live-aligned
- `symphonyAPI.stopSymphony` -> `POST /api/symphony/stop` -> live-aligned
- `symphonyAPI.processEmpathy` -> `POST /api/empathy/process` -> broken by live runtime
- `symphonyAPI.analyzeVietnameseText` -> `POST /api/vietnamese/analyze` -> broken by live runtime

- `userAPI.getUserDetails` -> `GET /api/users/:id` -> declared but unproven in source, broken by current live runtime
- `userAPI.updateUserDetails` -> `PUT /api/users/:id` -> declared but unproven in source, broken by current live runtime
- `userAPI.deleteUser` -> `DELETE /api/users/:id` -> declared but unproven in source, broken by current live runtime
- `userAPI.createUser` -> `POST /api/users` -> declared but unproven in source, broken by current live runtime

- `vietnameseNLP.analyzeVietnameseText` -> `POST /api/vietnamese/analyze` -> broken by live runtime
- `vietnameseNLP.generateCulturalContent` -> `POST /api/vietnamese/generate` -> declared but unproven in source, broken by current live runtime

## Live-Aligned Calls

- `symphonyAPI.getSymphonyMetrics`
- `symphonyAPI.startSymphony`
- `symphonyAPI.stopSymphony`

## Broken Or Drift Calls

- Entire chat lane is fallback-only and not backend-backed:
  - `chatAPI.receiveMessages`
  - `chatAPI.sendMessage`
- Entire empathy lane is broken against current live runtime:
  - `empathyAPI.*`
- Entire Vietnamese lane is broken against current live runtime:
  - `vietnameseNLP.*`
- Cross-domain duplicates in `symphonyAPI.ts` are broken outside the live symphony core:
  - `symphonyAPI.processEmpathy`
  - `symphonyAPI.analyzeVietnameseText`
- Dormant source-defined user and NotebookLM clients are not live in current runtime:
  - `userAPI.*`
  - `notebooklmAPI.*`

## Unknowns

- Whether the currently running `backend/server.js` differs from the source snapshot on disk beyond the symphony routes already proven live
- Whether the non-live lanes are intentionally disabled, partially booted, or shadowed by another runtime mode
- Whether `symphonyAPI.getSymphonyStatus` is intentionally dormant or simply unused

## Next Checks

- Probe each symphony endpoint again when runtime state changes to confirm stability
- If a future task targets empathy, Vietnamese, user, or NotebookLM lanes, re-probe those endpoints before trusting source declarations
- If client repair is requested, start with:
  - `src/services/api/empathyAPI.ts`
  - `src/services/api/vietnameseNLP.ts`
  - `src/services/api/chatAPI.ts`
  - then active consumers in hooks and contexts

## Delta: Runtime flag enforcement (2026-03-28)

- Added `src/services/runtimeFlags.ts` to centralize the `VITE_ENABLE_*` toggles so the quarantine state is kept in one place and shared across APIs, websockets, and feature toggles.
- `src/services/api/userAPI.ts` and `src/services/api/notebooklmAPI.ts` now import those flags directly and throw consistent errors when invoked without the live runtime enabled.
- `src/hooks/useWebSocket.ts` now exposes `connect`, `disconnect`, and `runtimeEnabled`, uses the shared flag, and `src/components/visualization/SymphonyVisualizer.tsx` surfaces the quarantine state, connection status, and inline notes about the non-live websocket lane.

## Delta: Quarantine Candidates For Non-Live Lanes

Smallest set of files that should be marked inactive or guarded first, using live-runtime truth only:

- `src/services/api/empathyAPI.ts`
  - quarantine entire empathy lane at service boundary
- `src/services/api/vietnameseNLP.ts`
  - quarantine entire Vietnamese lane at service boundary
- `src/services/api/chatAPI.ts`
  - mark chat as explicit local-only fallback, not live backend
- `src/contexts/EmpathyContext.tsx`
  - guard active empathy consumer against non-live lane assumptions
- `src/hooks/useEmpathy.ts`
  - guard polling path that currently assumes live empathy status
- `src/hooks/useVietnameseNLP.ts`
  - guard active Vietnamese request path

Second-wave quarantine targets only if broader UI signaling is needed:

- `src/pages/Analytics.tsx`
  - depends on empathy analytics lane
- `src/pages/VietnameseAnalysis.tsx`
  - depends on Vietnamese lane
- `src/components/chat/ChatInterface.tsx`
  - currently works by fallback, should be labeled non-live if product wants explicit runtime honesty

Dormant but non-live lanes that do not need first-wave quarantine because they are not meaningfully wired into active UI:

- `src/services/api/userAPI.ts`
- `src/services/api/notebooklmAPI.ts`

Websocket note:

- websocket lanes are not proven live in this cycle
- no websocket-specific quarantine target was added in first wave because this capsule is restricted to API/client choke points already traced

## Delta: Next Smallest Service-Level Quarantine

Next quarantine targets after empathy and Vietnamese service-boundary quarantine:

- `src/services/api/userAPI.ts`
  - mark entire user CRUD lane inactive against current live runtime truth
  - reason: endpoints are source-declared but not proven live and are not meaningfully exercised by active UI

- `src/services/api/notebooklmAPI.ts`
  - mark entire NotebookLM lane inactive against current live runtime truth
  - reason: endpoints are source-declared but not proven live and are not wired into active product flow

Websocket-adjacent client assumptions to quarantine next:

- `src/hooks/useWebSocket.ts`
  - treat websocket runtime as unproven until explicit live endpoint evidence exists

- `src/services/websocket/chatSocket.ts`
  - mark chat websocket lane non-live/unproven

- `src/services/websocket/metricsSocket.ts`
  - mark metrics websocket lane non-live/unproven

- `src/services/websocket/symphonyLive.ts`
  - mark live-stream symphony websocket lane unproven even though HTTP symphony control lane is live

Why this is still minimal:

- `userAPI.ts` and `notebooklmAPI.ts` are service choke points for dormant non-live lanes
- websocket-adjacent quarantine is best applied at hook/service boundary before touching any pages or visualization consumers

## Delta 2026-03-30 Dynamic Runtime Authority Adoption

- Frontend API clients no longer have to stay pinned to the bundle-time backend origin.
- `src/services/runtimeConfig.ts` now holds a mutable runtime authority snapshot with local persistence and managed-runtime adoption helpers.
- `src/services/api/runtimeAPI.ts` now:
  - reads runtime capabilities from the current authority
  - adopts `managed_backend_url` automatically when runtime authority says to reuse or reconcile the managed path
  - falls back to the default authority if the adopted managed authority becomes unreachable
- `autonomyAPI.ts`, `symphonyAPI.ts`, `chatAPI.ts`, `userAPI.ts`, `empathyAPI.ts`, `vietnameseNLP.ts`, and `notebooklmAPI.ts` now resolve `getApiBaseUrl()` at call time instead of freezing API URLs at module load.
- Operational implication:
  - browser-shell routine decisions can follow the active local-first runtime authority without operator relay or a rebuild just to change ports
  - app-boundary autonomy is no longer blocked by stale import-time backend URLs

## Delta 2026-04-01 Autonomous Policy Authority

- `/api/autonomy/policy` is now part of the live app-core contract and should be treated as the browser-safe authority snapshot.
- current selected action: `reuse_default_runtime`
- current boundary state: `autonomous`
- backend classification: `autonomous-core-ready`
- frontend classification: `preview-alive`
- recent proof events:
- reuse_default_runtime: Default local runtime already satisfies the autonomous core contract.
- hold_current_runtime: Current backend listener is already running outside the default authority port, so nested recovery is skipped. Managed runtime manifest is missing or incomplete.
- reuse_default_runtime: Default local runtime already satisfies the autonomous core contract.
## Delta 2026-04-17 Preservation Cycle Runtime Probe

- Fresh runtime probes from the preservation cycle showed the current `backend/server.js` listener on `5000` responds successfully to:
  - `GET /api/health`
  - `GET /api/symphony/status`
  - `GET /api/autonomy/status`
  - `POST /api/vietnamese/analyze`
  - `GET /api/empathy/status`
  - `GET /api/notebooklm/status`
  - `GET /api/users/:id`
- Contract implication:
  - older quarantine notes that treated empathy, Vietnamese, NotebookLM, and users as uniformly broken are no longer current runtime truth
  - websocket lanes remain unproven
  - chat remains degraded/local-only rather than newly promoted to live-backed
- Execution decision:
  - this was runtime-proof refresh only, not an executable code change
  - no queue item advanced because `memory/master_autonomous_todo.md` has no pending app-surface item unlocked by this probe alone
