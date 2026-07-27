# AIOS Autonomous OODA Workflow

Date: 2026-04-16

## Purpose

HyperAI autonomy is not a one-shot operator action. It exists when the core runtime loop continuously observes the local ecosystem, orients against memory and registry, decides which worker surfaces should receive tasks, acts through those workers, records proof, and learns back into memory.

Machine-readable workflow:

`runtime/federation_orchestrator/autonomous_ooda_workflow.json`

Executable OODA runner:

`tools/hyperai_ooda_loop.py`

## Loop Stack

```text
Autonomous Loop
-> OODA Loop
-> Agent 1-6 Chain
-> Worker Runtime Execution
-> Proof / Closure
-> Memory Update
```

### Autonomous Loop

The autonomous loop preserves local runtime truth:

- `tools/hyperai_autonomous_cycle.py`
- `tools/hyperai_autonomous_daemon.py`

It proves whether the local product boundary is alive and whether routine runtime preservation is safe.

### OODA Loop

The OODA loop distributes work:

```text
Observe -> Orient -> Decide -> Act
```

- Observe: runtime scan, preservation cycle, worker policy, ecosystem registry.
- Orient: classify task, map surfaces through `phi_i(M)`, read AIDEV genesis/core lineage as source capability, not authority.
- Decide: choose preservation-only, agent-chain mission, block, or defer.
- Act: dispatch to Agent 1-6 and worker surfaces, then write proof and closure.

### Agent Chain

Agent 1-6 remains the proof-producing chain:

```text
Agent 1 scope
-> Agent 2 runtime
-> Agent 3 API
-> Agent 4 composition
-> Agent 5 verification
-> Agent 6 synthesis/closure
```

## Worker Surfaces

Codex, OpenClaw, VS Code, MCP connectors, local provider facades, local model substrates, and AIDEV-derived candidates are worker or candidate surfaces.

They do not become authority because they receive input or have capabilities.

Codex input for HyperAI work means:

```text
Codex = active worker/operator surface
not mission root by default
not product authority
not external delivery authority
```

## AIDEV / Genesis / Core Binding

`C:\Users\pc\aidev` is source-capability lineage:

- `hyperai_phoenix/app/genesis.py`: Genesis/control hub lineage.
- `core_system`: autonomous executor, monitor, feedback, validation concepts.
- `unified_hyperai_system`: orchestrator/function-bank lineage.
- `quantumreason_v3`: provider facade/reasoning lineage.

These sources inform OODA orientation, but they are not promoted wholesale into live authority without fresh proof.

## Correct Operating Rule

For governed HyperAI work, the correct worker-facing command is:

```text
python tools/hyperai_ooda_loop.py --task "<creator task>" --once
```

This command lets the core loop create a mission and distribute work before any implementation handoff.

Use lower-level commands only when explicitly diagnosing a layer:

- `python tools/hyperai_autonomous_cycle.py`: preservation only.
- `python tools/hyperai_autonomous_cycle.py --agent-chain`: bridge proof for one mission.
- `python tools/hyperai_agent_dispatch.py`: low-level dispatch creation.
- `python tools/hyperai_agent_worker_loop.py`: low-level worker execution.

## Drift Rule

If a worker directly edits or concludes without OODA or agent-chain proof, report it as worker assistance, not autonomous HyperAI operation.

If a task produces system understanding, update memory.
