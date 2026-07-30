# Agent 4 Frontend Composition Capsule

## Scope

- Product surface only: `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`

## Route Map

- `/` -> `Dashboard`
- `/chat` -> `Chat`
- `/symphony-control` -> `SymphonyControl`
- `/settings` -> `Settings`
- frozen direct routes are no longer exposed in the public shell:
  - `/vietnamese-analysis`
  - `/analytics`

## Provider Topology

- `Router -> EmpathyProvider -> SymphonyProvider -> UserProvider -> ThemeProvider -> Switch`
- `EmpathyProvider`: empathy processing output state
- `SymphonyProvider`: symphony metrics/status polling state
- `UserProvider`: local user and preferences state
- `ThemeProvider`: local theme toggle state

## Live Paths

- `Dashboard -> SymphonyDashboard -> symphonyAPI -> /api/symphony/status`
- Active backend runtime truth for frontend alignment: `backend/server.js`

## Degraded Paths

- `Chat -> ChatInterface -> chatAPI` fallback behavior only
- Chat UI can render, but current live runtime truth does not prove chat backend contract

## Broken-By-Contract Paths

- Websocket client files under `src/services/websocket/` do not match current live backend/runtime ports or contracts
- Empathy, Vietnamese, User, and NotebookLM frontend paths are declared in source but are not part of the strict live symphony-only lane

## Next Checks

- Reconcile `NavigationBar.tsx` with actual route map
- Keep `App.tsx` route exposure aligned to live-backed product truth
- Recheck dashboard/symphony lane first before touching degraded or unproven UI paths

## Delta 2026-03-28

### Safe Against Non-Live Backend Lanes

- `Dashboard.tsx` is safe only for the symphony-backed subset
- `SymphonyDashboard.tsx`
- `SymphonyContext.tsx`
- `useSymphony.ts`
- `symphonyAPI.ts`
- `useMetrics.ts` is safe as local synthetic data only

### Degraded Because Backend Is Non-Live Or Unproven

- `Chat.tsx`
- `ChatInterface.tsx`
- `chatAPI.ts`
- reason: chat falls back locally when backend messages route is absent

### Freeze Because They Depend On Non-Live APIs

- `VietnameseAnalysis.tsx`
- `useVietnameseNLP.ts`
- `vietnameseNLP.ts`
- `EmpathyContext.tsx`
- `useEmpathy.ts`
- `empathyAPI.ts`
- `userAPI.ts`
- `notebooklmAPI.ts`
- reason: these paths are declared in source but are outside the strict live symphony-backed lane and should not drive product-facing decisions without fresh backend proof

### Immediate Implication

- Keep the product centered on `Dashboard` plus the symphony lane
- Treat chat as degraded
- Freeze Vietnamese, empathy, user API, and NotebookLM frontend execution paths until their backend lanes are re-proven live

## Delta 2026-03-28 Freeze Map Cycle 2

### Next Smallest Freeze Or Labeling Targets

- `Settings.tsx`
- `UserProfile.tsx`
- `SettingsPanel.tsx`
- `userAPI.ts`
- action: freeze API-backed user narrative and keep any remaining user surface explicitly local-only until backend user lane is re-proven live

- `notebooklmAPI.ts`
- any future page or component that elevates NotebookLM into primary navigation
- action: keep NotebookLM out of product-facing route or navigation decisions; label as non-core integration only

- `chatSocket.ts`
- `metricsSocket.ts`
- `symphonyLive.ts`
- action: freeze all websocket client files as non-authoritative runtime surfaces; do not route users or feature work through them until port and contract truth are re-established

- `Chat.tsx`
- `ChatInterface.tsx`
- `chatAPI.ts`
- action: keep chat visible only as degraded or fallback-backed lane, never as equal to the live symphony core

### Priority Order

1. freeze websocket client surfaces from product-facing interpretation
2. label chat lane as degraded-only
3. freeze user API-backed settings/profile narrative
4. keep NotebookLM out of primary UI exposure

## Delta: Websocket visualization quarantine

- `useWebSocket` now reports runtime availability, connect/disconnect helpers, and surface errors while honoring the shared websocket runtime flag.
- `SymphonyVisualizer.tsx` consumes the hook to show explicit quarantine notices, connection status, and fallback messaging so the visualization does not imply a proven live websocket lane. Additional CSS (`visualizerContainer`, `statusLine`, `quarantineNotice`, `loadingLine`) was added so the quarantine copy stays visually consistent.

## Delta: Runtime classification cockpit

- Added `RuntimeStatePanel` to `Dashboard.tsx` so the browser now polls `/api/runtime/state`, shows the Dormant/Recoverable/Operational/Autonomous classification, and renders heartbeat/probe proofs next to the autonomy narrative. The panel always leans on the API’s proof summary instead of assuming static human narration.

## Delta 2026-03-28 Shell Truth Cycle

### Product-Facing Labels Landed

- `NavigationBar.tsx`
  - primary navigation is now centered on:
    - `Dashboard`
    - `Symphony Control`
    - `Chat (degraded)`
    - `Settings (local only)`
  - non-live lanes are removed from primary navigation exposure

- `Dashboard.tsx`
  - now states that the dashboard is the currently live symphony-backed runtime lane
  - now warns that chat is degraded and settings are local-only

- `Chat.tsx`
  - now declares degraded local mode explicitly

- `Settings.tsx`
  - now declares local-only persistence explicitly

### Runtime Result

- `npm run ci:build` passed after shell labeling changes
- `npm run ci:browser-smoke` passed on rerun against the current local preview/backend state

## Delta 2026-03-28 Autonomous Shell Consolidation

- `Dashboard.tsx` no longer centers empathy visualization inside the primary live shell.
- `Dashboard.tsx` now declares frozen lanes explicitly instead of presenting empathy telemetry as part of the live core.
- `SymphonyControl.tsx` is now reduced to a single live control surface through `SystemController`.
- Duplicate `FrequencyTuner` and `SymphonyDashboard` rendering was removed from `SymphonyControl.tsx`.

### Runtime Result

- `npm run ci:build` passed after dashboard and symphony shell consolidation
- `npm run ci:browser-smoke` passed after dashboard and symphony shell consolidation

## Delta 2026-03-28 Route Exposure Freeze

- `App.tsx` now keeps the public shell limited to:
  - `/`
  - `/chat`
  - `/symphony-control`
  - `/settings`
- frozen lanes remain in source but are no longer routed in the public shell:
  - analytics
  - Vietnamese analysis
- Operational implication:
  - truthful shell now depends on route exposure, not only page copy
  - direct product-facing navigation is aligned to the live symphony core, degraded chat lane, and local-only settings lane

## Delta 2026-03-28 Runtime Authority Cockpit

- `RuntimeLaneStatus.tsx` now surfaces backend runtime authority metadata from `/api/runtime/capabilities`.
- The shell now warns when the live backend listener is stale relative to `backend/server.js`.
- `Dashboard.tsx` and `SymphonyControl.tsx` now frame the shell as an autonomy-and-symphony command plane while keeping non-core browser lanes quarantined until deliberate promotion.

## Delta 2026-03-30 Autonomous Browser Boundary

- `src/contexts/AutonomyContext.tsx` is now the authoritative browser-side policy layer for the app boundary.
- Refresh order now is:
  - get runtime capabilities first
  - let runtime authority adoption happen before other API reads
  - then load autonomy status, objectives, and decisions from the selected authority
- Browser-shell safe recovery now stays inside the app boundary:
  - `reconcile-runtime` when runtime recovery says a managed path should be started or reused
  - `start-runtime` or `tick-runtime` when the active authority is recoverable but safe to continue locally
  - `mark-healthy` when the boundary is already operational/autonomous and only needs heartbeat confirmation
- The result is closer to the HAIOS `autonomous` definition:
  - routine app-boundary decisions are handled by the shell itself
  - runtime state is classified locally with memory continuity
  - recovery stays explicit and safe instead of depending on per-step operator relay

## Delta 2026-03-30 Main App Boundary Classification

- `src/contexts/AutonomyContext.tsx` now treats backend runtime classification as first-class authority for the browser boundary.
- Browser boundary behavior now includes:
  - persisted local-first autonomy snapshots
  - cooldown-based safe recovery
  - refresh-after-action synchronization for start/stop/tick/heartbeat flows
  - runtime reconciliation when backend authority reports managed-runtime recovery instead of a simple autonomy tick
- `src/components/control-panel/AutonomyPanel.tsx` now surfaces:
  - boundary state
  - recovery action
  - routine runtime decisions reported by backend authority
- Operational implication:
  - the main app boundary now classifies itself as dormant, recoverable, operational, or autonomous from live runtime proof rather than only from local polling state

## Delta 2026-03-30 Boundary Autonomy Surfacing

- `RuntimeLaneStatus.tsx` now polls runtime capabilities instead of reading them once at mount.
- The browser shell now renders:
  - HAIOS boundary state from `/api/runtime/capabilities`
  - recovery status and selected recovery action
  - last runtime launch timestamp when a safe recovery pass is in flight
- `AutonomyContext.tsx` now treats runtime reconciliation as part of safe browser-side recovery:
  - if the boundary is recoverable because authority is stale or managed runtime is missing, the browser can request `POST /api/runtime/reconcile`
- once boundary proof returns healthy and fresh, the browser can persist the boundary as `autonomous` without operator relay

## Delta 2026-03-30 Managed Frontend Promotion

- `src/contexts/AutonomyContext.tsx` now promotes the browser shell to the managed frontend boundary when runtime capabilities prove that:
  - a managed frontend URL exists
  - the managed runtime is healthy
  - the current browser origin is not already that managed boundary
- Promotion behavior preserves:
  - pathname
  - query string
  - hash
- `src/services/api/runtimeAPI.ts` now adopts a healthy managed backend authority directly from the runtime reconcile response instead of waiting for a later poll cycle.
- Operational implication:
  - the app boundary no longer stops at backend authority adoption
  - when local-first recovery needs the managed fallback lane, the browser shell completes the authority handoff without operator relay

## Delta 2026-03-30 Browser Boundary Auto-Recovery Guard

- `src/contexts/AutonomyContext.tsx` now auto-recovers the autonomy loop when the browser boundary sees a recoverable `standby` or `recovering` state.
- Auto-recovery stays local-first and safe:
  - browser shell will restart the autonomy loop itself instead of waiting for the operator to relay `start autonomy`
  - a manual stop now writes a local pause window so the browser does not immediately override explicit operator intent
  - a manual start clears the pause and returns the boundary to self-healing mode
- Verification status for this delta:
  - `npm run ci:build` passed
  - direct browser smoke passed against a fresh managed backend/frontend pair on `5006/4179`
- Remaining blocker:
  - `runtime:autonomous:start` is still not consistently writing the managed runtime manifest after isolated boot, even when the managed pair becomes reachable and smoke passes manually

## Delta 2026-03-30 Browser Boundary Manual-Pause Safety

- `src/contexts/AutonomyContext.tsx` now preserves explicit operator intent:
  - manual stop writes a local pause window
  - browser-side safe recovery will not immediately restart autonomy during that pause window
  - manual start clears the pause and returns the shell to self-healing mode
- `scripts/ci/browser-agent-smoke.mjs` now restores the original symphony/autonomy state after exercising start/stop and verifies symphony transitions through backend state instead of brittle UI-only status text.
- Operational implication:
  - browser verification no longer leaves the main boundary in `standby`
  - the app shell can keep proving `autonomous` after CI smoke instead of degrading itself as a side effect of verification

## Delta 2026-04-01 Autonomous Authority Surfacing

- `AutonomyContext.tsx` and `AutonomyPanel.tsx` should treat `/api/autonomy/policy` as the UI-facing authority artifact for routine runtime decisions.
- The main shell remains limited to the autonomy-safe core while policy proof events explain default vs managed authority changes.
- current runtime story: `runtime_cleanup` with boundary `projection_missing`
- runtime strategy: `local_first_probe`
## Delta 2026-04-17 Preservation Cycle

- Browser/runtime proof remains:
  - `/` shell on `4173` is reachable
  - boundary state remains `autonomous`
  - selected action remains `reuse_default_runtime`
- Current frontend interpretation should stay:
  - dashboard, symphony, runtime, and autonomy are the primary shell
  - chat stays degraded/local-only
  - websocket clients stay frozen/unproven
- Runtime probe update:
  - backend now answers `empathy`, `vietnamese`, `notebooklm`, and `users` HTTP probes successfully
  - this does not by itself promote those lanes into primary route exposure or remove the existing shell narrowing
