# AIOS Runtime Orchestration Memory Deployment - 2026-05-16

Status: DEPLOYED_LOCAL_BRIDGE
Mutation class: runtime orchestration files + memory receipt
Secrets: none recorded

## Canon Decision

Codex Desktop runtime remains untouched. The repair layer is local MCP/dynamic bridge plus skill-first mission routing.

Runtime contract:

`MISSION -> SKILL_DISCOVERY -> SKILL_SELECTION -> SKILL_EXECUTION -> VERIFY -> CONTINUE_QUEUE`

The previous degraded pattern is blocked:

`MISSION -> SHELL_SCAN -> REPORT -> STOP`

## Active Artifacts

| artifact | path | role |
|---|---|---|
| master skill | `/Users/andy/.agents/skills/hyperai-runtime-orchestrator/SKILL.md` | skill-first mission router law |
| router CLI | `/Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py` | packet builder and memory bridge |
| MCP server | `/Users/andy/workbench/aios_runtime_orchestrator/mcp_server.py` | dynamic bridge exposing AIOS tools |
| Codex config | `/Users/andy/.codex/config.toml` | registers `AIOS_MISSION_ROUTER` |
| restore kit | `/Users/andy/workbench/aios_runtime_orchestrator/restore` | factory reset recovery source |
| client shell | `/Users/andy/workbench/aios-runtime-orchestrator-client` | clean Electron packet UI |
| cwd context | `/Users/andy/Documents/MacOSMac/AGENTS.md` | imports Canon and route law |
| queue | `/Users/andy/HyperAI-Sync/memory/runtime_execution_todo.md` | continuation queue |

## Tool Interfaces

- `aios.memory.load`
- `aios.skills.route`
- `aios.mission.plan`
- `aios.queue.append`
- `aios.verify.run`

## Verification Evidence

Executed locally:

- Python compile: PASS
- Unit tests: 5 tests PASS
- Router verify: PASS
- Codex config TOML parse: PASS
- MCP initialize/tools/list/tools/call: PASS
- Electron static JS check: PASS

Router verify proves:

- `hyperai-runtime-orchestrator` exists.
- `system-scan-ctx-gam` exists.
- Canon exists.
- `.con-memory/conversations.db` exists and is readable read-only.
- `HyperAI-Sync/memory` exists.
- Runtime router selects `hyperai-runtime-orchestrator` first.
- Shell-first behavior is blocked until route exists.

## Restore Rule

After reset, restore `/Users/andy/workbench` and `/Users/andy/HyperAI-Sync`, then follow:

`/Users/andy/workbench/aios_runtime_orchestrator/restore/README.md`

Do not restore or print secrets. Do not touch `/Users/andy/.codex/auth.json`.
