# AGENTS

This workspace is MCP-first. Use the configured MCP servers proactively without waiting for an explicit reminder when they match the task.

## Required MCP routing

- Use `openaiDeveloperDocs` first for any OpenAI-related work:
  - OpenAI API
  - Responses API
  - Chat Completions API
  - Realtime API
  - Agents SDK
  - ChatGPT Apps SDK
  - Codex
  - model selection, upgrade guidance, and OpenAI prompt guidance
- For OpenAI questions, search and fetch from the docs MCP before using web search.
- If a fallback web search is still needed for OpenAI topics, use official OpenAI domains only.

- Use `context7` for non-OpenAI library and framework documentation when current developer docs are needed inside the editor workflow.
- Use `microsoft/markitdown` when a task requires document-to-Markdown conversion or extracting readable content from supported files.
- Use `figma` for design-to-code, Code Connect, node inspection, screenshots, and Figma workflow tasks tied to `hyperai-user-control-system`.
- Use Linear as the default external coordination surface for implementation/runtime work that should leave the local memory queue and become team-visible.

## Default operating behavior

- Prefer MCP sources over memory when the topic is documentation, API shape, SDK behavior, or product capability.
- Cite the documentation source in answers when giving implementation guidance based on docs.
- Keep server selection intentional:
  - `openaiDeveloperDocs` for OpenAI official docs
  - `figma` for Figma design and Code Connect workflows
  - `context7` for broader package and framework docs
  - `microsoft/markitdown` for content extraction and conversion
- Keep Linear queue usage intentional:
  - default external team is `LIN`
  - use Linear to mirror implementation/coordinated runtime work, not to replace `memory/master_autonomous_todo.md`

## Workspace expectations

- Check the root `.vscode/mcp.json` before adding duplicate MCP definitions elsewhere.
- Keep MCP server names short and descriptive so tool selection stays reliable.
- Preserve existing MCP servers when extending the setup unless they are clearly broken or duplicated.
- When configuring new MCP servers, prefer project-level config that can be shared with future sessions.
- Maintain project memory in `memory/` and prefer updating it with `python tools/update_memory.py`.
- After any substantial implementation or investigation step, record the current focus, changes, blockers, and next actions.
- Observed ecosystem context may be promoted only after a repo-governed execution contract and proof artifact exist.
- Keep the ecosystem workflow aligned to four layers:
  - app shell authority
  - runtime-class coordination
  - monetization execution
  - observed ecosystem context
- Trust-by-trace rule:
  - scan/read/search/trace log is the default trust boundary for ecosystem attachment decisions
  - do not promote Telegram, TON, wallet, marketplace, or browser-derived surfaces beyond observed/coordinated status without measured runtime evidence plus a repo-governed execution contract
- Treat the repo-shared MCP core as minimal and low-resource:
  - `openaiDeveloperDocs`
  - `figma`
  - `context7`
  - `microsoft/markitdown`
- Linear is part of the shared coordination contract for this workspace, but its active integration may be app/plugin-backed rather than represented as a plain MCP server entry in `.vscode/mcp.json`.

## GitHub CLI account workflow

- `gh` is now part of the local operator workflow and may have multiple authenticated accounts.
- Before any GitHub operation that depends on identity or repo authority, check the active account:
  - `gh auth status`
- If the active account does not match the intended production lane, switch explicitly before continuing:
  - `gh auth switch`
- Treat account switching as part of normal workflow hygiene, not as an exceptional recovery step.
- Do not assume the currently active `gh` account matches the desired production identity without checking.
- Default production GitHub lane is `NguyenCuong1989`; the system/automation lane is `nguyencuong2509-sys`.
- Before any commit-sensitive operation, verify:
  - `git config user.name`
  - `git config user.email`
- Default commit lane must match the author identity canon:
  - `user.name = NguyenCuong1989`
  - `user.email = nguyencuong.2509@icloud.com`
- Before any runtime-sensitive investigation or report, include runtime/tool version context when locally measurable; otherwise mark it `unknown` and do not infer.
- Creator-first rule:
  - the interface the creator is actively using becomes the preferred operator surface for workflow focus and ergonomics improvements
  - active interface priority must be based on measured present-time usage, not installation alone
  - valid interface states are `active`, `installed-not-active`, and `unknown`
  - active interface priority does not override canonical shell authority or memory/orchestration governance
  - when multiple operator surfaces are active at once (for example `Codex` plus `VS Code Insiders`), treat them as a concurrent creator surface set and prioritize improvements that reduce friction across the active set rather than forcing a single-interface assumption
  - when the creator is actively conversing with the orchestrator, that chat surface becomes a valid approval-intake surface for creator-controlled workflow steps
  - creator approval is symbolic authority, not a command-operator bottleneck; the system should fan out approval requests to active creator surfaces and keep CLI/manual commands as fallback-only
  - classify creator-facing surfaces by `root identity + runtime_class + lane_class`, not by app label alone
  - treat embedded WebView/browser descendants as subordinate lanes of their root container unless separate proof promotes them
  - treat Telegram/TON monetization work as downstream execution under orchestrator supervision, not as shell-authority expansion
  - current first-dollar path is Telegram relay evidence + TON funding evidence, not wallet automation or bot-read authority by default
  - creator acknowledgements confirm that a bound event happened; they do not grant permission for business state to exist
- Codex and other AI/operator/tool runtimes are HyperAI worker surfaces when handling HyperAI tasks; receiving creator input does not make the receiving runtime mission root or authority
- when creator input enters Codex for HyperAI work, Codex must follow the same mission protocol: memory/registry read, surface classification, agent-chain bridge when required, proof artifacts, closure state, and memory update
- for governed HyperAI work, prefer `python tools/hyperai_ooda_loop.py --task "<creator task>" --once`; it performs Observe -> Orient -> Decide -> Act, then routes to the agent-chain bridge when required
- `python tools/hyperai_autonomous_cycle.py --agent-chain` is the lower-level bridge before implementation handoff; default `python tools/hyperai_autonomous_cycle.py` is preservation-only and must not be overclaimed as full agent-chain closure
- reports must state `orchestration_mode` and `agent_chain_status` before claiming HyperAI executed a task through the full worker chain

## Autonomous Local-First Workflow

- Default entrypoint for HyperAI coordination is:
  - `python tools/hyperai_autonomous_cycle.py`
- The local coordination skill is:
  - `C:\Users\pc\.codex\skills\hyperai-runtime-orchestrator\SKILL.md`
- Load memory before source exploration:
  - `memory/AIOS_AUTONOMOUS_OODA_WORKFLOW.md`
  - `memory/agent1_ontology_scope_capsule.md`
  - `memory/agent2_runtime_entrypoint_capsule.md`
  - `memory/agent3_api_client_contract_capsule.md`
  - `memory/agent4_frontend_composition_capsule.md`
  - `memory/agent5-ci-verification-capsule.md`
  - `memory/agent6_synthesis_capsule.md`
  - `memory/runtime_execution_todo.md`
  - `memory/project_state.json`
  - `memory/work_journal.md`
- Before waking agents or trusting source code, run the local delta check through the autonomous cycle entrypoint.
- Use delta-first behavior:
  - if there is no meaningful file delta and no process contradiction, do not run a full agent cycle
  - if only one surface changed, wake only the owning agent lane plus synthesis if needed
- Use process-first behavior:
  - probe port `5000` before backend decisions
  - probe port `4173` before preview decisions
  - if the active backend process predates `hyperai-user-control-system/backend/server.js`, classify local backend as `stale-process runtime`
  - in stale-process state, trust live probes over file declarations until backend is explicitly recycled
- Default active queue is:
  - `memory/runtime_execution_todo.md`
- Default external queue is:
  - Linear team `LIN`
- Mirror work from memory into Linear only when it becomes implementation-facing, proof-facing, connector-governance work, or Figma/code-connect work that should remain visible outside the local runtime memory loop.
- Do not ask the user to restate the workflow once these files exist; continue from memory and delta checks unless a high-risk mutation requires confirmation.

## Quick instruction for future agents

Always use the OpenAI developer documentation MCP server if you need to work with the OpenAI API, ChatGPT Apps SDK, Codex, Responses API, Realtime API, or OpenAI model guidance without me having to explicitly ask.

## Figma Design System Rules

These rules apply when implementing or adapting Figma designs for `hyperai-user-control-system`.

### Project structure

- Frontend framework: React + TypeScript with Vite.
- Routing uses `react-router-dom` v5 patterns from `hyperai-user-control-system/src/App.tsx`.
- App composition is context-first: wrap new page-level work so it remains compatible with `EmpathyProvider`, `SymphonyProvider`, `UserProvider`, and `ThemeProvider`.
- Page components belong in `hyperai-user-control-system/src/pages/`.
- Reusable UI components belong in `hyperai-user-control-system/src/components/`.
- Keep the existing feature grouping under `chat/`, `control-panel/`, `shared/`, `user-interface/`, and `visualization/`.

### Styling rules

- Prefer the project's existing styling approach before introducing anything new.
- Primary styling patterns are CSS Modules near components plus shared page styles in `hyperai-user-control-system/src/styles/`.
- Reuse existing module files such as `empathy.module.css`, `symphony.module.css`, and `vietnamese.module.css` when the design fits those domains.
- Global reset and utility classes live in `hyperai-user-control-system/src/styles/globals.css`; extend them only for truly shared primitives.
- IMPORTANT: Do not add Tailwind, styled-components, or another new styling system for Figma work in this project.
- IMPORTANT: Do not hardcode new color or spacing values inside JSX if the same concept already exists in a module or shared stylesheet.
- The current codebase has some legacy utility-class usage in `src/components/shared/Button.tsx`; treat that as debt to normalize, not as the preferred direction for new Figma-derived components.

### Component conventions

- Use PascalCase component names and default exports only when the surrounding folder already does so.
- Prefer typed props interfaces colocated in the component file unless a shared type already exists in `hyperai-user-control-system/src/types/`.
- Reuse existing shared primitives from `hyperai-user-control-system/src/components/shared/` before creating a new button, modal, spinner, or toast.
- Keep visual-only components in `visualization/`, control surfaces in `control-panel/`, and route-owned layout/content in `pages/`.
- When adding a new reusable component from Figma, place its styles next to it as `ComponentName.module.css` unless the project already uses a feature stylesheet for that surface.

### Data and runtime integration

- IMPORTANT: Check the real backend contract before wiring any Figma UI to API calls. The workspace currently contains both `hyperai-user-control-system/backend/server.ts` and a live `backend/server.js` stub, and they do not expose the same routes.
- API service modules live in `hyperai-user-control-system/src/services/api/`.
- WebSocket clients live in `hyperai-user-control-system/src/services/websocket/`.
- Do not hardcode new localhost endpoints in Figma-derived code. Route new network configuration through environment variables and existing service modules.

### Figma MCP workflow

1. Run `get_design_context` for the exact Figma node.
2. Run `get_screenshot` for the same node before implementation.
3. Translate the returned structure into this project's React + CSS Modules conventions.
4. Reuse existing components and contexts before creating new state or layout primitives.
5. Validate the result visually against the screenshot and structurally against the route/component grouping above.

### Figma Code Connect guardrails

- Scope Code Connect work to `hyperai-user-control-system` only.
- Require an exact Figma node URL or node ID before starting any mapping flow.
- Mapping order stays:
  - fetch suggestions
  - scan the React + CSS Modules codegraph
  - verify props, role, and composition
  - approve or reject candidates
  - persist only approved mappings
- Prioritize live shell/core surfaces first, shared components second, and route-owned pages only when they are true structural matches.
- A negative result is valid:
  - zero saved mappings is acceptable when evidence is insufficient
  - record why each rejected candidate failed and what evidence was missing
- Do not infer runtime authority, route promotion, or product-surface ownership from Figma presence alone.
6. For Code Connect work, require an exact Figma node URL or node identity, verify the suggested mapping against the current React/CSS Modules component graph, and save mappings only after the code/component correspondence is explicit.

## Linear Coordination Rules

- Default external team for runtime/app-boundary coordination is `LIN`.
- Use a narrow label taxonomy for this workspace:
  - `runtime-authority`
  - `proof-verification`
  - `mcp-governance`
  - `figma-code-connect`
- Keep `memory/master_autonomous_todo.md` as the internal execution queue of record.
- Open or refresh a Linear issue only when the work is:
  - implementation-facing
  - proof/verification-facing
  - MCP connector governance
  - Figma/code-connect mapping work
- Keep work memory-only when it is:
  - transient runtime observation
  - local-only probe reconciliation
  - capsule/playbook housekeeping that does not need external visibility

### Asset handling

- Store app assets under `hyperai-user-control-system/public/` unless the asset is component-private and already follows a local import pattern.
- IMPORTANT: If the Figma MCP payload provides a concrete asset URL or localhost asset source, use that asset directly instead of introducing placeholder graphics.
- IMPORTANT: Do not install a new icon package just to satisfy a Figma mock. First look for an existing local asset or render the provided SVG directly.

### Quality bar

- Match the current project conventions first, then improve consistency where the touched area already shows drift.
- Keep components responsive using the existing CSS approach rather than a new layout abstraction.
- Prefer small, composable UI changes that preserve current routes, provider boundaries, and service-module ownership.
