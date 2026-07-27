# AIOS Runtime Class Matrix - 2026-04-15

This matrix consolidates runtime-class ownership from the federation capability matrix, unified registry, dependency graph, and economy planning artifacts.

## Matrix

| Node | Runtime class | Family / lane | Current status | Allowed roles | Forbidden roles | Evidence source | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `root_host_substrate` | physical Windows host | root substrate | degraded/conservation-critical | root preservation, local filesystem custody | disposable runtime, purge target | `memory/AIOS_ROOT_HOST_CONSERVATION_WARNING_20260415.md` | stop destructive recovery, reset, purge |
| `shell_authority` | service_runtime | shell_orchestrator | degraded | mission_root, execution_adapter, evidence_recorder | lineage_only | `runtime/federation_orchestrator/unified_registry.json`; `tools/hyperai_autonomous_cycle.py` | stop economy and shell mutation expansion |
| `haios_runtime` | service_runtime | runtime_orchestrator | dormant/recoverable | mission_root, mission_router, evidence_recorder, behavior_delegate | lineage_only | `runtime/federation_orchestrator/mission_authority_policy.json` | stop if root host unsafe |
| `federation_orchestrator` | service_runtime | federation_orchestrator | usable for planning | mission_root, mission_router, evidence_recorder, behavior_delegate | lineage_only | `runtime/federation_orchestrator/*.json` | stop on critical drift |
| `memory_writer` | service_runtime | memory_registry | live | memory_write | shell mutation, ledger mutation | `tools/update_memory.py`; memory freshness in `unified_registry.json` | stop if memory blocked |
| `verification_truth` | service_runtime | verification_registry | live as registry | runtime_probe, ci_build, browser_smoke | business authority | `.github/workflows/ci.yml`; runtime probes | stop if verification unavailable |
| `provider_reasoning` | service_runtime | reasoning_orchestrators | live | reasoning_delegate | mission_root, approval_intake, execution_adapter, evidence_recorder | QuantumReason `/api/v2/health`; `unified_registry.json` | stop on provider down for rank/format |
| `gemini_cli` | service_runtime | reasoning_orchestrators | policy-listed, not primary active surface | reasoning_delegate, behavior_delegate, approval_intake | execution_adapter, evidence_recorder | `mission_authority_policy.json`; `orchestrator_capability_matrix.json` | stop if no measured active proof |
| `deal_intelligence` | service_runtime | economy/deal lane | degraded | filter, rank, format under orchestration | shell authority, ledger authority | `runtime/deal_intelligence/deal_intelligence_state.json`; `workflow_registry.json` | stop when shell degraded |
| `agent3_api` | service_runtime | API reasoning lane | degraded | classify, rank, summarize, format | execution authority | `runtime/llm_augmentation/agent3_api/*.json` | stop when shell degraded |
| `agent5_ci` | service_runtime | CI reasoning lane | degraded | summarize, classify, rank, format, verification reasoning | CI truth replacement | `runtime/llm_augmentation/agent5_ci/*.json` | stop when shell degraded |
| `agent6_synthesis` | service_runtime | synthesis lane | degraded | summarize, format | execution authority | `runtime/llm_augmentation/agent6_synthesis/*.json` | stop when shell degraded |
| `telegram_relay` | service_runtime | distribution_registry | live registry, blocked by shell degraded | publish_relay, publish_confirm | shell authority, business truth creation | `runtime/telegram_node/telegram_registry.json`; `unified_registry.json` | stop when shell degraded |
| `telegram_execution_fabric` | service_runtime | monetization_orchestrators | policy node | execution_adapter, evidence_recorder, observer_only | mission_root, lineage_only | `mission_authority_policy.json`; `orchestrator_capability_matrix.json` | stop without shell authority and creator proof |
| `treasury_control` | service_runtime | monetization_orchestrators | live registry, receive-only | execution_adapter, evidence_recorder, balance/funding read | approval_intake, spending authority, lineage_only | `runtime/federation_orchestrator/treasury_registry.json`; `unified_registry.json` | stop when shell degraded |
| `chatgpt_desktop` | desktop_electron_runtime | creator_surface_orchestrators | active approval-capable surface by policy class | approval_intake, observer_only | execution_adapter, evidence_recorder | `orchestrator_capability_matrix.json`; drift guard collision | no autonomous execution |
| `codex_desktop` | desktop_electron_runtime | creator_surface_orchestrators | active working surface | approval_intake, reasoning_delegate, observer_only | execution_adapter, evidence_recorder, mission_root | current session; `orchestrator_capability_matrix.json` | no autonomous shell or ledger authority |
| `chrome_browser` | browser_runtime | creator_surface_orchestrators | active approval-capable surface by policy class | approval_intake, observer_only | execution_adapter, evidence_recorder | `orchestrator_drift_guard.json` | subordinate to root container |
| `edge_browser` | browser_runtime | creator_surface_orchestrators | active approval-capable surface by policy class | approval_intake, observer_only | execution_adapter, evidence_recorder | `orchestrator_drift_guard.json` | subordinate to root container |
| `aidev_lineage_root` | archive_runtime | observed_ecosystem_orchestrators | observed lineage root | observer_only, lineage_only | mission_root, approval_intake, execution_adapter, evidence_recorder | `runtime/federation_orchestrator/orchestrator_dependency_graph.json`; runtime todo attachment phase | no promotion without proof and rollback contract |

## Current Routing Consequence

Because `shell_authority` is degraded, the matrix permits planning, memory consolidation, creator approval intake, and read-only attachment review. It blocks economy execution, publish confirmation, funding detection, treasury proposal, and any runtime expansion that would depend on Docker/WSL/HCS or shell mutation.

