# ACTIVE DISPATCH REPORT
*Generated: 2026-07-30T23:29:27Z*
*Execution hash: 065677fa372d69e705d835e191338be3f75bf093608745347546f145b02ee92f*

## Executive Summary
- Processes observed: 100
- Registry nodes: 35
- Operationally qualified: 28/35
- OpenAI credential rotated: 2026-07-30T23:14:25.620805+00:00
- Titan/MacMini Ollama projections: STANDBY_UNREACHABLE
- Unknown unbound processes: 0

## Capability Map Summary
| node | base_app | lanes | host | state | mission |
|---|---|---|---|---|---|
| apo_upstream_macbook_ollama | macbook_ollama | KNOWLEDGE | MACBOOK_ACTIVE | ACTIVE | operate apo_upstream_macbook_ollama as KNOWLEDGE |
| apo_upstream_titan_ollama | titan_ollama | KNOWLEDGE | TITAN_STANDBY | STANDBY_UNREACHABLE | operate apo_upstream_titan_ollama as KNOWLEDGE |
| apo_upstream_macmini_ollama | macmini_ollama | KNOWLEDGE | MACMINI_STANDBY | STANDBY_UNREACHABLE | operate apo_upstream_macmini_ollama as KNOWLEDGE |
| apo_upstream_lmstudio | lmstudio | KNOWLEDGE | MACBOOK_ACTIVE | ACTIVE | operate apo_upstream_lmstudio as KNOWLEDGE |
| openapi_tool_time | time | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_time as EXECUTION |
| openapi_tool_weather | weather | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_weather as EXECUTION |
| openapi_tool_filesystem | filesystem | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_filesystem as EXECUTION |
| openapi_tool_git | git | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_git as EXECUTION |
| openapi_tool_memory | memory | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_memory as EXECUTION |
| openapi_tool_quotes | quotes | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_quotes as EXECUTION |
| openapi_tool_flashcards | flashcards | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_flashcards as EXECUTION |
| openapi_tool_time_ui | time_ui | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_time_ui as EXECUTION |
| openapi_tool_summarizer | summarizer | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_summarizer as EXECUTION |
| openapi_tool_bitcoin | bitcoin | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_bitcoin as EXECUTION |
| openapi_tool_sql | sql | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_sql as EXECUTION |
| openapi_tool_external_rag | external_rag | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_external_rag as EXECUTION |
| openapi_tool_slack | slack | COMMUNICATION,EXECUTION,KNOWLEDGE | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_slack as COMMUNICATION/EXECUTION/KNOWLEDGE |
| openapi_tool_google_pse | google_pse | KNOWLEDGE,EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate openapi_tool_google_pse as KNOWLEDGE/EXECUTION |
| mcp_pieces | pieces | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate mcp_pieces as EXECUTION |
| mcp_docker_mcp | docker_mcp | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate mcp_docker_mcp as EXECUTION |
| credential_broker | /Users/andy/HyperAI-Sync/tools/hyperai_credentials_service.py | AUTH | MACBOOK_ACTIVE | ACTIVE | operate credential_broker as AUTH |
| apo_gateway | bash | ROUTING | MACBOOK_ACTIVE | ACTIVE | operate apo_gateway as ROUTING |
| agent_os_dashboard | bash | PLANNING,EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate agent_os_dashboard as PLANNING/EXECUTION |
| lmstudio_bionic_api | node | KNOWLEDGE | MACBOOK_ACTIVE | ACTIVE | operate lmstudio_bionic_api as KNOWLEDGE |
| bionic_app | Bionic | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate bionic_app as EXECUTION |
| ollama_macbook | Squirrel | KNOWLEDGE | MACBOOK_ACTIVE | ACTIVE | operate ollama_macbook as KNOWLEDGE |
| pieces_mcp | open | EXECUTION | MACBOOK_ACTIVE | ACTIVE | operate pieces_mcp as EXECUTION |
| finalai | /Users/andy/.local/bin/finalai-openai-proxy.py | KNOWLEDGE | MACBOOK_ACTIVE | ACTIVE | operate finalai as KNOWLEDGE |
| redis_local | redis-server | MEMORY | MACBOOK_ACTIVE | ACTIVE | operate redis_local as MEMORY |
| hyperai_product_runtime | backend/server.js | PRODUCT | MACBOOK_ACTIVE | STALE | operate hyperai_product_runtime as PRODUCT |
| docker_desktop | com.docker.virtualization | INFRASTRUCTURE | MACBOOK_ACTIVE | ACTIVE | operate docker_desktop as INFRASTRUCTURE |
| federation_orchestrator | /Users/andy/HyperAI-Sync/runtime/federation_orchestrator | ROUTING,PLANNING | UNKNOWN_UNBOUND | UNKNOWN_UNBOUND | operate federation_orchestrator as ROUTING/PLANNING |
| memory_writer | tools/update_memory.py | MEMORY | UNKNOWN_UNBOUND | UNKNOWN_UNBOUND | operate memory_writer as MEMORY |
| codex_operator_runtime | /Users/andy/.codex/config.toml | EXECUTION | UNKNOWN_UNBOUND | UNKNOWN_UNBOUND | operate codex_operator_runtime as EXECUTION |
| aios_mission_router | /Users/andy/workbench/aios_runtime_orchestrator/mcp_server.py | ROUTING | MACBOOK_ACTIVE | ACTIVE | operate aios_mission_router as ROUTING |

## Auth Recovery Status
- **openai**: COMPLETED — broker /status healthy: openai
- **openapi_tool_slack**: PLANNED — GET /health on openapi_tool_slack + broker /status slack healthy
- **openapi_tool_google_pse**: PLANNED — GET /health on openapi_tool_google_pse + broker /status google_pse healthy

## Compute Ledger Summary
- DAIOF: 100 processes, 3782475776 bytes RSS

## Value Flow
- source → creator intent + OS processes
- interpret/plan → ROUTING lane
- execute → AUTH → KNOWLEDGE → EXECUTION/COMMUNICATION → PRODUCT
- verify → SECURITY + VERIFICATION lanes
- record → MEMORY lane

## Stopping Conditions
- Any external provider returns 401/403 after credential rotation.
- Broker /status returns openai unhealthy.
- Canon change attempted without receipt or rollback path.
- Plaintext secret detected in any artifact.