## Current focus

- Lock ontology and working scope for `hyperai-user-control-system`.
- Lock the new autonomous local-first workflow into ontology scope.
- Lock stale-process startup semantics into ontology scope.
- Keep ontology delta aligned with `runtime_execution_todo.md` and Agent 2 runtime memory.

## Verified truths

- Default active product surface is `C:\Users\pc\HyperAI_Phoenix_Master\hyperai-user-control-system`.
- Trusted ontology surfaces are:
  - `AGENTS.md`
  - `memory/repo-playbook.md`
  - `memory/hyperai-user-control-system-playbook.md`
  - `memory/agent-topology-playbook.md`
  - `memory/runtime_execution_todo.md`
  - `memory/agent2_runtime_entrypoint_capsule.md`
  - `.vscode/mcp.json`
- Documented backend runtime truth is `hyperai-user-control-system/backend/server.js`.
- MCP routing truth is:
  - `openaiDeveloperDocs` for OpenAI topics
  - `context7` for non-OpenAI docs
  - `microsoft/markitdown` for document extraction
- Autonomous local-first workflow is now explicit:
  - default coordination entrypoint is `python tools/hyperai_autonomous_cycle.py`
  - memory must be loaded before source exploration
  - use delta-first behavior before waking a full agent cycle
  - default active queue is `memory/runtime_execution_todo.md`
  - if there is no meaningful file delta and no process contradiction, do not run a full agent cycle
- Startup semantics are now explicit in AGENTS and playbooks:
  - probe port `5000` before backend decisions
  - if process start time is older than `backend/server.js` last modified time, classify backend as `stale-process runtime`
  - in stale-process state, trust live probes over file declarations until backend is explicitly recycled
- Runtime todo confirms this ontology delta has already been accepted:
  - `Reconcile stale backend process rule into runtime playbook and skill flow` is marked done
- Agent 2 runtime capsule confirms stale-process reality:
  - live port `5000` process predates current `backend/server.js`
  - `dispatch_backend_live.log` `EADDRINUSE` is treated as supporting evidence for the old listener still owning the port
  - active backend reasoning must start from live port ownership and minimal endpoint probes, not file declarations alone

## Not verified

- No live process probe was run in the current cycle.
- No current check confirmed whether port `5000` is still occupied now.
- No runtime code execution was performed in this memory-first cycle.

## Conflicts

- Previous ontology gap has narrowed:
  - canonical backend path and stale-process handling are now both documented
- Remaining ontology tension:
  - file truth still names `backend/server.js` as canonical backend runtime
  - process truth may still diverge from current file contents if the backend has not been recycled
- Locked operational resolution:
  - under local-first workflow, process-first probing wins before startup or backend reasoning
  - `backend/server.js` remains file canon, but not sufficient proof of live behavior without a fresh process check

## Next actions

- Preserve ontology scope to `hyperai-user-control-system` and the listed memory/MCP surfaces.
- Preserve autonomous local-first behavior as the default coordination ontology.
- Before any future backend reasoning, load runtime memory and apply the stale-process probe rule first.
- Treat `memory/runtime_execution_todo.md` as the default autonomous queue for local cycles.
- Only escalate beyond ontology surfaces if a later cycle needs fresh live-runtime confirmation.

## Delta 2026-04-15 Ecosystem Sync Canon

- Added `memory/AIOS_ECOSYSTEM_SYNC_CANON.md` as the ontology gate for whole-ecosystem coordination.
- Added `memory/AIOS_RUNTIME_CLASS_MATRIX_20260415.md` to classify root host, shell authority, federation, memory, verification, provider reasoning, economy, treasury, creator surfaces, and lineage/archive nodes by runtime class and allowed mission roles.
- Locked the current root-host conservation rule into ecosystem ontology:
  - Windows host remains the root substrate.
  - Docker/WSL/HCS recovery is not an expansion basis while degraded.
  - `shell_authority` degraded state blocks economy execution and runtime expansion.
- Future ecosystem work must bind to a mission template before execution and must respect one mission root plus one evidence recorder.

## Delta 2026-04-15 Sprint 1 G(t) Reduction

- Added `memory/AIOS_G_REDUCTION_SPRINT_PLAN.md` as the ontology plan for lowering ecosystem noise without runtime mutation.
- Added `memory/AIOS_ROOT_HOST_DEPLOYMENT_CHECKLIST.md` as a preflight gate before root-host, runtime, economy, ledger, or archive-affecting actions.
- Locked Sprint 1 ontology:
  - reduce `G(t)` through classification and stop-rule proof
  - preserve `T`, `W`, and `F`
  - do not trade root-host safety for runtime expansion
  - require mission-template binding before any future action

## Delta 2026-04-15 AIOS Invariants

- Added `memory/AIOS_INVARIANTS.md` as the hard invariant canon for all AIOS/HyperAI decisions.
- Added `runtime/federation_orchestrator/aios_invariants.json` as the machine-readable invariant registry.
- Invariant ontology now covers:
  - root-host conservation
  - single mission root and authority
  - single evidence recorder and memory writer
  - verification truth gate
  - shell authority and runtime safety
  - economy invariants and `blocked_cleanly`
  - lane separation
  - invariant-under-failure behavior
  - mandatory re-audit of `T`, `G(t)`, `Th`, `W`, `F`, `D`, and `Trust(S)`

## Delta 2026-04-15 VS Code / Extension Degraded-Shell Policy

- Added `memory/AIOS_VSCODE_EXTENSION_DEGRADED_SHELL_POLICY.md`.
- Added `runtime/federation_orchestrator/vscode_extension_degraded_shell_policy.json`.
- Ontology rule:
  - VS Code, extensions, editor agents, and IDE copilots are creator/operator surfaces, not shell authority.
  - Under `shell_authority=degraded`, commands must classify as `allowed`, `approval_required`, or `blocked`.
  - Unknown command classes fail closed as `approval_required`.

## Delta 2026-04-15 Creator-AI Coexistence Workflow

- Added `memory/AIOS_CREATOR_AI_COEXISTENCE_WORKFLOW.md`.
- Added `runtime/federation_orchestrator/creator_ai_coexistence_workflow.json`.
- Ontology update:
  - authority is a cartographic placement label, not domination
  - creator conservation precedes root-host conservation, invariant preservation, runtime recovery, economy execution, and expansion
  - AIOS capabilities exist to reduce creator burden and preserve the living system, not to pressure creator decisions
  - sediment is preserved by default and stratified rather than erased

## Delta 2026-04-15 Model-Native Runtime Canon

- Added `memory/AIOS_MODEL_NATIVE_RUNTIME_CANON.md`.
- Added `runtime/federation_orchestrator/model_native_runtime_registry.json`.
- Ontology update:
  - `M = {P,t,H(t),T,G(t),Th,F,W,D,Trust(P)}` is now a model-native operating contract, not only an audit prompt.
  - `AI_RUNTIME` must map each runtime, tool, cloud, Git, and model surface as `phi_i(M)` before promotion or execution.
  - `U_model` measures direct model understanding; `K_runtime = g(C,E,R)` measures useful transformation while preserving constraints.
  - model language cannot override root-host conservation, proof gates, dirty Git protection, or cloud/Docker stop rules.

## Delta 2026-04-15 Local Codex Operator Runtime

- Added `memory/AIOS_LOCAL_CODEX_OPERATOR_RUNTIME.md`.
- Added `runtime/federation_orchestrator/local_codex_operator_runtime.json`.
- Ontology correction:
  - the current creator conversation surface is a customized local Codex/AIOS operator runtime, not just `hyperai-user-control-system`
  - observed local layers include skills, plugins, MCP routing, automations, rules, memories, sessions, sandboxing, cache/state, project memory, and runtime governance artifacts
  - product runtime, operator runtime, and root-host substrate are coupled but not identical

## Delta 2026-03-30 Autonomous Boundary Claim

- `hyperai-user-control-system` can now claim `autonomous` at the primary app boundary only when:
  - `backend/server.js` is the fresh listener on `5000`
  - `4173` is reachable for the active browser shell
  - `/api/autonomy/status` and `/api/runtime/capabilities` both report a healthy autonomy-safe core
- Managed isolated runtime is now ontology support, not primary ontology truth, when the default local-first boundary is already fresh and smoke-clean.
- HAIOS wording should now distinguish:
  - `5000/4173` fresh + smoke-clean -> autonomous boundary
  - managed runtime present because default authority is stale or missing -> recoverable-to-autonomous through safe recovery

## Delta 2026-04-16 Unified Memory-Bound Workflow

- Added ontology responsibility for `memory/AIOS_UNIFIED_MEMORY_BOUND_WORKFLOW.md`.
- Added machine-readable workflow registry at `runtime/federation_orchestrator/unified_memory_bound_workflow.json`.
- Agent 1 responsibility:
  - ensure every material task starts with formal/canonical memory load
  - map input to `M / phi_i(M)`
  - identify broken mapping or missing formal canon before execution
  - preserve `Output = Transformation(M)` rather than answer-only handling

## Delta 2026-04-16 Ecosystem Runtime Registry

- Added ontology responsibility for `memory/AIOS_ECOSYSTEM_RUNTIME_REGISTRY_20260416.md`.
- Added machine-readable registry at `runtime/federation_orchestrator/aios_ecosystem_runtime_registry.json`.
- Agent 1 responsibility:
  - prevent flattening AI systems, app runtimes, operator cockpits, provider fabrics, memory, verification, and downstream lanes into one executor pool
  - require each surface to declare runtime class, authority class, proof source, stop condition, promotion rule, and control interface before routing
  - treat physical process/server consolidation as separate from capability/authority registry consolidation

## Delta 2026-04-18 Creator Alignment Working Set

- Added `memory/AIOS_CREATOR_ALIGNMENT_WORKING_SET_20260418.md`.
- Added `runtime/federation_orchestrator/creator_alignment_working_set.json`.
- Agent 1 responsibility:
  - bind the active Codex surface as a creator-alignment worker cockpit during architecture-tightening phases
  - require structure-first parsing and memory-first execution for creator-facing HyperAI work
  - treat text-only runtime claims as insufficient when live probes are feasible
  - require explicit `orchestration_mode` and `agent_chain_status` in execution reports
