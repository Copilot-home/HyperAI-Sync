# AIOS Ecosystem Runtime Registry

## Purpose

This canon records the standardized registry layer for HyperAI/AIOS operation across local AI systems, app runtimes, operator cockpits, provider fabrics, tools, verification, memory, and downstream execution lanes.

HyperAI/AIOS is not one app server and not a flat executor pool. It is a local-first unified execution system that upgrades, uses, operates, and optimizes AI systems, apps, and software runtimes for the creator's workflow.

Machine-readable registry:

`runtime/federation_orchestrator/aios_ecosystem_runtime_registry.json`

## Operating Model

Every surface is mapped before use:

```text
surface -> phi_i(M) -> runtime_class -> authority_class -> proof_source -> allowed_action
```

Useful capability does not imply authority. Each surface must declare:

- runtime class
- authority class
- owner surface
- capabilities
- allowed roles
- forbidden roles
- proof source
- stop conditions
- promotion rule
- control interface when applicable

## Registry Groups

Current standardized surface groups:

- `hyperai_product_runtime`: product shell authority for proven app lanes on `5000/4173`
- `app_core_lanes`: dashboard, symphony, runtime, autonomy
- `app_non_core_lanes`: empathy, Vietnamese, NotebookLM, users
- `app_degraded_frozen_lanes`: chat local-only, websocket frozen, `backend/server.ts`, managed fallback
- `federation_orchestrator`: mission routing, drift guard, policy registry
- `memory_writer`: canonical lightweight memory updates through `tools/update_memory.py`
- `verification_truth`: runtime probe, CI build, browser smoke, proof validation
- `codex_operator_runtime`: customized local AIOS/Codex operator cockpit
- `openclaw_control_lane`: OpenClaw operator/control lane through `tools/openclaw_control.py`
- `local_fakeapi_provider_fabric`: QuantumReason OpenAI-compatible local facade
- `ollama_local_models`: local model substrate
- `mcp_connectors`: connector-specific capability graph
- `vscode_operator_surface`: editor/operator surface under degraded-shell policy
- `git_sync_transport`: sync transport, not automatic authority
- `gcp_cloud_observed`: observed cloud substrate
- `telegram_treasury_economy`: downstream execution lanes, blocked or gated

## Hard Rules

- Do not merge physical processes just to make the control model look simple.
- Consolidate capability and authority through registry and wrappers first.
- Do not promote OpenClaw, Codex, VS Code, Ollama, MCP, Git, cloud, or app non-core lanes by label or installation alone.
- When creator input enters Codex or another registered runtime for HyperAI work, that runtime is a worker surface of HyperAI, not an authority shortcut.
- All side-effect surfaces require mission binding, proof, rollback, and memory update.
- OpenClaw device/phone/channel/cron/external delivery stays blocked until a dedicated contract opens it.
- App runtime `5000/4173` remains product shell authority only for proven core lanes.

## Next Use

Before routing a task, load:

1. `runtime/federation_orchestrator/aios_ecosystem_runtime_registry.json`
2. `runtime/federation_orchestrator/mission_authority_policy.json`
3. `runtime/federation_orchestrator/unified_memory_bound_workflow.json`

Then bind one mission root, one router, one evidence recorder, and the narrowest valid execution surface.

For multi-agent HyperAI operation, dispatch the mission through:

```text
python tools/hyperai_agent_dispatch.py --title "<mission>" --description "<contract>" --action-class route --surface <surface_id>
```

The dispatcher writes:

- `runtime/federation_orchestrator/agent_task_dispatch_registry.json`
- `runtime/federation_orchestrator/agent_task_dispatch_proofs/*.json`

This is the required path when HyperAI should coordinate Agent 1-6 instead of the local operator surface acting as a single coding bot.

## Agent Worker Loop

The dispatch registry is now executable through:

```text
python tools/hyperai_agent_worker_loop.py --mission-id <mission_id>
python tools/hyperai_agent_worker_loop.py --run-next
python tools/hyperai_agent_worker_loop.py --close-ready
```

The worker consumes assigned dispatch missions, runs Agent 1-6 only when dependencies are complete, writes per-agent proof JSON under `runtime/federation_orchestrator/agent_task_outputs/<mission_id>/`, and lets Agent 6 close the mission with a route plan under `runtime/federation_orchestrator/agent_route_plans/`.

The worker is governance-only. It may update dispatch registry state, agent output artifacts, route plans, and memory/canon. It must not mutate product app source code, external delivery surfaces, phone/device lanes, cloud state, wallet/ledger lanes, cron jobs, or broad host configuration.

## Worker Runtime Binding

Codex and other AI/operator/tool runtimes are workers of HyperAI when the task belongs to the HyperAI ecosystem. Receiving the user's input does not make the receiving runtime the mission root or execution authority.

Machine-readable policy:

`runtime/federation_orchestrator/worker_runtime_binding_policy.json`

Required interpretation:

- Input into Codex for HyperAI work means Codex acts as `codex_operator_runtime`, a worker/operator surface.
- Codex should read memory/registry, classify the task, and use `python tools/hyperai_ooda_loop.py --task "<creator task>" --once` when the task should be distributed by the HyperAI core.
- `python tools/hyperai_autonomous_cycle.py --agent-chain` remains the lower-level bridge used by the OODA loop when Agent 1-6 closure is required.
- Codex may still perform bounded implementation only after the generated route plan opens that lane and verification gates are known.
- Reports must quote `orchestration_mode` and `agent_chain_status` before claiming that HyperAI executed the task.
- A direct preservation-only cycle is not full `Dispatch -> Agent_Chain -> Proof -> Closure`.

## Autonomous OODA Workflow

Autonomous operation is now defined as:

```text
Autonomous preservation loop
-> OODA task distribution loop
-> Agent 1-6 proof chain
-> worker runtime execution
-> closure and memory update
```

The OODA workflow binds AIDEV genesis/core lineage into orientation without promoting it to current authority:

- `hyperai_phoenix/app/genesis.py`: Genesis/control hub lineage
- `core_system`: autonomous executor/monitor/validation concepts
- `unified_hyperai_system`: orchestrator/function-bank lineage
- `quantumreason_v3`: provider facade/reasoning lineage

Machine-readable workflow:

`runtime/federation_orchestrator/autonomous_ooda_workflow.json`
