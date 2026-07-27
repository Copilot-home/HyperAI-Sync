# HyperAI Phoenix Master Repo Playbook

## Purpose

This workspace is a super-workspace, not a clean monorepo. It contains active product code, historical control surfaces, backup trees, archived repos, vendor content, and generated artifacts. Future sessions should use this file to avoid selecting the wrong runtime or verification path.

## Default Working Scope

- Default workspace root: `C:\Users\pc\HyperAI_Phoenix_Master`
- Default product surface for implementation, debugging, and verification:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`
- Do not default to broad recursive scans from the workspace root.
- When searching, prefer bounded scans inside `hyperai-user-control-system` unless the task explicitly targets archive, memory, or infrastructure surfaces.

## Product Surface Canon

- App manifest:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\package.json`
- Frontend runtime entrypoints:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\src\main.tsx`
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\src\App.tsx`
- Backend runtime path actually used by CI and Docker:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\backend\server.js`
- Backend TypeScript surface exists, but is not the current CI runtime:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\backend\server.ts`

## Source Of Truth

- Primary CI contract:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\.github\workflows\ci.yml`
- Delivery packaging:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\.github\workflows\cd.yml`
- Release packaging:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\.github\workflows\release.yml`
- Identity normalization:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\.github\workflows\identity-surface.yml`
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\scripts\ci\configure_git_identity.py`
- Browser smoke contract:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\scripts\ci\browser-agent-smoke.mjs`
- Root MCP config:
  - `C:\Users\pc\HyperAI_Phoenix_Master\.vscode\mcp.json`
- Repo-shared MCP core:
  - `openaiDeveloperDocs`
  - `figma`
  - `context7`
  - `microsoft/markitdown`
- Shared external coordination queue:
  - Linear team `LIN`
- Long-running multi-agent coordination contract:
  - `C:\Users\pc\HyperAI_Phoenix_Master\memory\agent-topology-playbook.md`

## Known Traps

- `backend/server.ts` is not the current CI runtime path.
- `backend/server.ts` is currently frozen as non-executable architecture until an explicit backend-unification task is opened.
- `hyperai-user-control-system/README.md` has operational drift:
  - uses `yarn`
  - points to `localhost:3000`
- Root `package.json` is not the app entrypoint.
- Root `.vscode/tasks.json` points at `_CONSOLIDATED/VSCode_Local/resources/app` and should not be treated as the product task source.
- Root `.vscode/launch.json` is only a generic remote attach stub, not proof of the active runtime layout.
- Legacy shell scripts under `hyperai-user-control-system/scripts/` still use `yarn` and are less trustworthy than CI workflows.
- The workspace contains many backup and archive trees, so unbounded file search can easily return false leads.

## Runtime Notes

- Frontend dev path uses Vite from `hyperai-user-control-system`.
- CI preview path uses `http://127.0.0.1:4173`.
- Backend smoke path uses `http://127.0.0.1:5000`.
- Current smoke expectations are:
  - `GET /api/health` returns status payload from `backend/server.js`
  - `GET /api/symphony/status` returns `empathy_circulation`
  - frontend body includes one of `Dashboard`, `User Profile`, or `Symphony Dashboard`

## Startup Semantics

- Probe port `5000` before starting or reasoning about the backend locally.
- If a listener already exists on `5000`, record:
  - owning PID
  - process command line
  - process start time
  - `backend/server.js` last modified time
- If the process start time is older than `backend/server.js` last modified time, classify local backend as `stale-process runtime`.
- In a `stale-process runtime` state:
  - do not trust file-declared routes as live behavior
  - use live probes against the running process for operational decisions
  - recycle the backend explicitly before expecting the process to reflect the current file on disk
- Default backend assumption remains the symphony-backed core unless a deliberate backend recycle re-proves broader routes.

## Runtime Lineage

- Current product surface:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`
- Current CI source of truth:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\.github\workflows\ci.yml`
- Current backend runtime:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system\backend\server.js`
- Gemini legacy status:
  - not active in the current product surface
- Remaining Google integration:
  - NotebookLM is still present as an optional integration surface
  - it is not the main runtime path or CI path
- Operational implication:
  - do not change or verify against Gemini-era paths unless the task explicitly touches the remaining NotebookLM integration files

## Governed Git Lineage

- Canonical operator shell stays:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`
- Control habitat stays:
  - `C:\Users\pc\HyperAI_Phoenix_Master`
- Preferred git lineage is:
  - `C:\Users\pc\aidev`
  - remote: `https://github.com/sowhat1989/aidev.git`
- Secondary lineage mirror is:
  - `C:\aios_project\aidev`
- Archive lineage mirrors are source-material only:
  - `AI_EMERGENCY_VAULT\aidev\aidev`
  - `_CONSOLIDATED\aidev`
- Attachment rule for future sessions:
  - keep the shell separate
  - do not use `git worktree`, `subtree`, `submodule`, or directory moves unless an explicit repo-attachment task is opened
  - do not promote archive mirrors over `C:\Users\pc\aidev` unless the preferred lineage becomes unreadable or invalid
  - keep GitHub mode as `filesystem-authority` until `gh` is present in `PATH` and a deliberate attach phase is approved

## App Boundary State

- `hyperai-user-control-system` should now be described as:
  - `autonomous` for the app core boundary
  - `operational but non-core` for probeable auxiliary lanes
- Autonomous-safe core:
  - dashboard
  - symphony control
  - runtime status
  - autonomy status
- Non-core operational lanes do not become primary shell lanes just because runtime probes pass.
- Chat remains `degraded/local-only`.
- Websocket clients remain frozen from authority claims.
- Broader ecosystem coordination is MCP-backed, but not yet a sovereign unified runtime.
- Observed ecosystem context may be promoted only after a repo-governed execution contract and proof artifact exist.

## Runtime-Class Coordination Canon

- Treat local apps as runtime manifolds, not as app-name entities.
- Canonical runtime classes for this phase are:
  - `desktop_electron_runtime`
  - `native_webview_runtime`
  - `browser_runtime`
  - `automation_runtime`
  - `service_runtime`
- Runtime identity truth is now written to:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\orchestrator\runtime_identity_registry.json`
- Route creator approval intake by:
  - `root_identity`
  - `runtime_class`
  - `lane_class`
  - `authority_role`
- Do not infer approval authority from app label alone.
- WebView/browser helper descendants remain embedded lanes unless separately proven.

## Ecosystem Workflow Canon

- Keep the ecosystem synchronized through four governed layers:
  - shell/app authority
  - runtime-class coordination
  - monetization execution
  - observed ecosystem context
- Shell/app authority remains:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`
  - `backend/server.js`
  - CI proof from `ci.yml`
- Runtime-class coordination remains:
  - `runtime/orchestrator/runtime_identity_registry.json`
  - `runtime/federation_orchestrator/creator_surface_policy.json`
  - `runtime/federation_orchestrator/approval_requests.json`
- Monetization execution for the current phase remains:
  - Telegram relay lane
  - TON receive-only treasury lane
  - creator-confirmed publish and funding events only
- Observed ecosystem context includes:
  - Telegram community/runtime presence
  - TON wallets and marketplaces
  - other local app runtimes not yet tied to a repo-governed execution contract
- Do not skip layers:
  - ecosystem context may inform routing and prioritization
  - only execution contracts plus proof artifacts may promote a surface into monetization execution or authority
- Current supreme mission is:
  - complete the first real Telegram publish confirmation
  - complete the first real TON funding confirmation
  - let `first_dollar_achieved` flip through canonical ledgers and metrics only
- Trust-by-trace rule for this phase:
  - measured process/runtime evidence is the default attachment boundary
  - queue state, ledgers, approval requests, and process traces outrank installation assumptions
  - ecosystem promotion requires both trace evidence and a repo-governed execution contract

## MCP And Queue Contract

- Figma is part of the repo-shared MCP core for design-to-code and Code Connect work.
- Linear is part of the shared coordination contract for this workspace and the default external queue is team `LIN`.
- Treat Figma and Linear as coordination infrastructure, not app-boundary runtime authority.
- Mirror work from `memory/master_autonomous_todo.md` into Linear only when it crosses one of these boundaries:
  - runtime authority implementation
  - proof/verification work
  - MCP connector governance
  - Figma/code-connect mapping work
- Keep work memory-only when it is limited to local probe truth, capsule maintenance, or internal queue hygiene.

## Creator Approval Contract

- The creator approval model is `creator-in-the-loop`, not `creator-as-cli-operator`.
- The creator role in Treasury.A1 is `fact confirmer`, not `business authority`.
- If the creator is actively using an orchestrator chat surface, that live chat becomes a valid approval-intake surface for creator-controlled steps.
- Treasury.A1 creator confirmations should therefore be modeled as:
  - system raises an approval request
  - active creator surfaces receive the request
  - creator acknowledges or rejects a bound event
  - runtime commits the result to the canonical ledger and phase-state artifacts
- Publish acknowledgement specifically requires:
  - exact `publish_event_id`
  - publish evidence reference
  - canonical ledger commit before the state machine may move past `awaiting_publish_evidence`
- CLI remains a valid fallback path, but not the preferred creator UX when a live orchestrator chat is already active.
- Approval relay surfaces do not become runtime authority; shell/app runtime remains the only execution authority.
- Do not treat the symbolic creator approval step as permission to skip ledger evidence, event IDs, or fail-closed validation.
- Active creator-surface policy is now written to:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\federation_orchestrator\creator_surface_policy.json`
- Treasury.A1 approval intake requests are now written to:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\federation_orchestrator\approval_requests.json`
- Current creator approval flow for the first-dollar mission is:
  - orchestrator detects `next_valid_operator_action`
  - orchestrator writes or refreshes the matching approval request by event id
  - active creator surfaces receive the request in priority order
  - creator acknowledgement resolves into the canonical ledger path
  - if delivery fails, CLI remains fallback-only and the request stays pending
- Chat, QR login, or session presence alone do not mutate business state.

## First-Dollar Runbook

- Canonical flow is:
  - `event -> evidence -> ledger -> metric`
- First-dollar publish path:
  - create `publish_event_id`
  - relay through Telegram
  - capture publish evidence or ack
  - bind creator acknowledgement to the exact event id
  - write publish ledger entry
- Telegram publish proof stays pending until the evidence reference is captured in the canonical publish path.
- First-dollar funding path:
  - create `funding_event_id`
  - capture TON funding evidence
  - bind creator acknowledgement to the exact event id
  - write treasury ledger entry
- Phase-switch rule:
  - only canonical ledger entries may update revenue metrics
  - only revenue metrics may flip `first_dollar_achieved`
  - only `first_dollar_achieved` may make `Treasury.B` eligible

## Telegram And TON Execution Contract

- Telegram is currently:
  - `native_webview_runtime`
  - relay surface
  - creator-visible execution focus for the first-dollar phase
- Telegram execution truth is now summarized in:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\telegram_node\telegram_execution_state.json`
- TON treasury is currently:
  - receive-only
  - manual-confirm
  - economic evidence lane, not shell authority
- TON receive evidence truth is now summarized in:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\treasury\ton_receive_evidence_state.json`
- Creator approval delivery truth is now summarized in:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\federation_orchestrator\approval_delivery_state.json`
- Do not over-claim the current machine truth:
  - Telegram content reading is not yet proven through a usable MCP or bot-execution connector in this session
  - the current proven Telegram path is relay + creator confirm
  - the current proven TON path is receive metadata + creator funding confirm
- Workflow priority for the current phase is therefore:
  1. keep runtime identity fresh
  2. keep creator approval requests aligned with active surfaces
  3. execute one real Telegram relay/publish
  4. execute one real TON funding confirmation
  5. let the canonical revenue artifacts flip the phase state

## Failover Drill Contract

- Dedicated runtime drill command:
  - `npm run runtime:autonomous:drill`
- Safe-drill preconditions:
  - `npm run runtime:autonomous:ensure` returns `reuse_default_runtime`
  - default authority is healthy on `5000/4173`
- Safe-drill sequence:
  - snapshot pre-drill authority from the runtime manifest, proof artifact, and live probes
  - withhold the default boundary in a bounded way
  - allow managed runtime only as temporary fallback evidence
  - restore default authority
  - re-prove the default path before any follow-on work
- Drill artifact:
  - `C:\Users\pc\HyperAI_Phoenix_Master\runtime\hyperai-failover-drill.json`
- Abort rule:
  - if the default authority does not recover cleanly after the drill, the artifact must still be written
  - Branch B Figma work must not start
  - memory must record `blocked by runtime safety`

## Figma Code Connect Contract

- Code Connect scope is limited to `hyperai-user-control-system`.
- Branch B starts with a reality-check gate, not with mapping:
  - scan repo and `memory/` for a stored Figma URL, `fileKey`, or `node-id`
  - confirm `.vscode/mcp.json` still contains the shared `figma` server
  - confirm Figma auth is live in the current MCP session
  - if the current tool surface still has no discoverable file/node listing path, conclude `node identity not discoverable from current environment`
- Exact Figma node URL or node ID is required before mapping work starts.
- Canonical mapping sequence:
  - fetch suggestions
  - scan the current React + CSS Modules codegraph
  - verify props, role, and composition
  - approve or reject candidates
  - persist approved mappings only
- Branch B may not infer component existence from Figma alone; codegraph evidence is required for any mapping.
- Zero approved mappings is a valid outcome when evidence is insufficient.
- The local memory summary must record:
  - why no mapping was approved
  - what evidence was missing
  - which candidates were rejected

## Verify Contract

Run verification from:

- `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`

Command order:

1. `npm run lint`
2. `npm test -- --runInBand`
3. `npm run ci:build`
4. `npm run ci:browser-smoke`

Current baseline observed locally:

- `npm run lint`: passes through the legacy wrapper, or skips with an explicit runtime-lane reason
- `npm test -- --runInBand`: passes through the legacy wrapper, or skips with an explicit runtime-lane reason
- `npm run ci:build`: passes
- `npm run ci:browser-smoke`: passes
- `python tools/hyperai_autonomous_cycle.py`: returns `state_transition: reuse_default_runtime`
- `GET /api/runtime/capabilities` reports:
  - `boundary_state: autonomous`
  - `autonomous_core_ready: true`
  - `requires_operator_relay: false`

CI nuance:

- `legacy-test-audit` in `ci.yml` is non-blocking with `continue-on-error: true`
- The strongest current merge confidence comes from `ci:build` and `ci:browser-smoke`

## Verify Matrix

### Frontend-only

- Required:
  - `npm run ci:build`
- Recommended:
  - `npm run lint`
  - `npm test -- --runInBand`
- Add:
  - `npm run ci:browser-smoke` when changes affect rendering, routing, or UI/backend contract behavior

### Backend-only

- Required:
  - `npm run ci:build`
- Recommended:
  - `npm test -- --runInBand`
  - `npm run lint`
- Add:
  - `npm run ci:browser-smoke` when changes touch `backend/server.js`, smoke endpoints, or API contracts used by the frontend

### Full-stack or shared contract

- Required:
  - `npm run ci:build`
  - `npm run ci:browser-smoke`
- Recommended:
  - `npm test -- --runInBand`
  - `npm run lint`

### Docs, memory, or non-runtime only

- Usually required:
  - no runtime verification
- Always report:
  - that runtime verification was not run
  - why the change does not affect executable paths

## Verify Semantics

- Hard gates right now:
  - `npm run ci:build`
  - `npm run ci:browser-smoke`
- Advisory signals right now:
  - `npm run lint`
  - `npm test -- --runInBand`
- Required execution directory:
  - `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`

## Reporting Contract

Every substantial task closeout should state:

- what changed
- what was verified
- what was not verified
- remaining risks or blockers

Preferred closeout template:

- Scope changed
- Runtime path affected
- Verified
- Not verified
- Remaining risk

## Memory Workflow

- Keep repo memory in `C:\Users\pc\HyperAI_Phoenix_Master\memory`
- Preferred update command:
  - `python tools/update_memory.py --focus "..." --summary "..." --next "..."`
- After substantial implementation or investigation, record:
  - current focus
  - changes or findings
  - blockers
  - next action
- When coordinating long-running parallel analysis or execution lanes, use:
  - `C:\Users\pc\HyperAI_Phoenix_Master\memory\agent-topology-playbook.md`
