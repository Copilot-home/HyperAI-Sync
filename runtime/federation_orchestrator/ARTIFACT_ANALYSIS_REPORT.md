# BÁO CÁO PHÂN TÍCH 7 ARTIFACT
*Tạo từ: `/Users/andy/HyperAI-Sync/runtime/federation_orchestrator`*
*Thời điểm audit: 2026-07-30T22:56:08.320939+00:00*
*Kết quả qualifier: **30 / 35** node operationally qualified*

## 1. Tổng quan hệ sinh thái runtime
- Tổng số process được quan sát: **103**
- Số node trong registry: **35**
- Đã qualified: **30**
- Chưa qualified: **5**
- Native app/process: **29**
- DAIOF AI projection (đã ánh xạ): **58**
- Unknown / chưa nhận diện: **16**

### Các node chưa qualified
| id | role | lý do | compute_claim |
|---|---|---|---|
| openapi_tool_slack | TOOL | auth:SLACK_BOT_TOKEN, auth:SLACK_TEAM_ID | process_group |
| openapi_tool_google_pse | TOOL | auth:GOOGLE_PSE_CX | process_group |
| mcp_docker_mcp | MCP | observed_runtime, role_resolved, authority_resolved, dependencies_resolved, health_probed | manual_or_recycle |
| hyperai_product_runtime | PRODUCT | observed_runtime, role_resolved, authority_resolved, dependencies_resolved, health_probed | manual_or_recycle |
| memory_writer | MEMORY | observed_runtime, role_resolved, authority_resolved, dependencies_resolved, health_probed | manual_or_recycle |

## 2. Ánh xạ process -> node / vai trò / authority
Bảng dưới liệt kê các process chính, node DAIOF, role, authority, owner.

| pid | name | owner | node | role | authority | ports | rss(bytes) |
|---|---|---|---|---|---|---|---|
| 787 | redis-server | redis | redis_local | MEMORY | OBSERVE,READ,WRITE | [6379] | 1196032 |
| 796 | Squirrel | apo_gateway | apo_upstream_macbook_ollama | PROVIDER | OBSERVE,INVOKE,READ | [] | 2211840 |
| 796 | Squirrel | apo_gateway | apo_upstream_titan_ollama | PROVIDER | OBSERVE,INVOKE,READ | [] | 2211840 |
| 796 | Squirrel | apo_gateway | apo_upstream_macmini_ollama | PROVIDER | OBSERVE,INVOKE,READ | [] | 2211840 |
| 796 | Squirrel | ollama | ollama_macbook | PROVIDER | OBSERVE,INVOKE,READ | [] | 2211840 |
| 807 | open | apo_gateway | mcp_pieces | MCP | OBSERVE,INVOKE,READ | [] | 3538944 |
| 807 | open | pieces | pieces_mcp | MCP | OBSERVE,INVOKE,READ | [] | 3538944 |
| 809 | Python | finalai | finalai | PROVIDER | OBSERVE,INVOKE,READ | [50520] | 3964928 |
| 809 | Python | redis | redis_local | MEMORY | OBSERVE,READ,WRITE | [50520] | 3964928 |
| 831 | Ollama | apo_gateway | apo_upstream_macbook_ollama | PROVIDER | OBSERVE,INVOKE,READ | [49196] | 14188544 |
| 831 | Ollama | apo_gateway | apo_upstream_titan_ollama | PROVIDER | OBSERVE,INVOKE,READ | [49196] | 14188544 |
| 831 | Ollama | apo_gateway | apo_upstream_macmini_ollama | PROVIDER | OBSERVE,INVOKE,READ | [49196] | 14188544 |
| 831 | Ollama | ollama | ollama_macbook | PROVIDER | OBSERVE,INVOKE,READ | [49196] | 14188544 |
| 864 | ollama | apo_gateway | apo_upstream_macbook_ollama | PROVIDER | OBSERVE,INVOKE,READ | [11434] | 8601600 |
| 864 | ollama | apo_gateway | apo_upstream_titan_ollama | PROVIDER | OBSERVE,INVOKE,READ | [11434] | 8601600 |
| 864 | ollama | apo_gateway | apo_upstream_macmini_ollama | PROVIDER | OBSERVE,INVOKE,READ | [11434] | 8601600 |
| 864 | ollama | ollama | ollama_macbook | PROVIDER | OBSERVE,INVOKE,READ | [11434] | 8601600 |
| 876 | Pieces OS | apo_gateway | mcp_pieces | MCP | OBSERVE,INVOKE,READ | [39300, 52140] | 240893952 |
| 876 | Pieces OS | pieces | pieces_mcp | MCP | OBSERVE,INVOKE,READ | [39300, 52140] | 240893952 |
| 2540 | zsh (kiro-cli-term) | redis | redis_local | MEMORY | OBSERVE,READ,WRITE | [] | 3276800 |
| 3852 | node | apo_gateway | apo_upstream_lmstudio | PROVIDER | OBSERVE,INVOKE,READ | [] | 11206656 |
| 3852 | node | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 11206656 |
| 8954 | lmlink-connector | apo_gateway | apo_upstream_lmstudio | PROVIDER | OBSERVE,INVOKE,READ | [50588] | 22298624 |
| 8954 | lmlink-connector | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [50588] | 22298624 |
| 11490 | bash | apo_gateway | openapi_tool_quotes | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 11491 | Python | apo_gateway | openapi_tool_quotes | TOOL | OBSERVE,INVOKE,READ | [8906] | 6586368 |
| 11511 | bash | apo_gateway | openapi_tool_flashcards | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 11512 | Python | apo_gateway | openapi_tool_flashcards | TOOL | OBSERVE,INVOKE,READ | [8907] | 6668288 |
| 11536 | bash | apo_gateway | openapi_tool_time_ui | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 11537 | Python | apo_gateway | openapi_tool_time_ui | TOOL | OBSERVE,INVOKE,READ | [8908] | 6635520 |
| 11978 | bash | apo_gateway | openapi_tool_summarizer | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 11979 | Python | apo_gateway | openapi_tool_summarizer | TOOL | OBSERVE,INVOKE,READ | [8909] | 7372800 |
| 12223 | bash | apo_gateway | openapi_tool_bitcoin | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 12224 | Python | apo_gateway | openapi_tool_bitcoin | TOOL | OBSERVE,INVOKE,READ | [8910] | 6651904 |
| 15562 | bash | apo_gateway | openapi_tool_sql | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 15563 | Python | apo_gateway | openapi_tool_sql | TOOL | OBSERVE,INVOKE,READ | [8911] | 7323648 |
| 24403 | bash | apo_gateway | openapi_tool_slack | TOOL | OBSERVE,INVOKE,READ | [] | 262144 |
| 24403 | bash | apo_gateway | openapi_tool_google_pse | TOOL | OBSERVE,INVOKE,READ | [] | 262144 |
| 24404 | bash | apo_gateway | openapi_tool_slack | TOOL | OBSERVE,INVOKE,READ | [] | 262144 |
| 24404 | bash | apo_gateway | openapi_tool_google_pse | TOOL | OBSERVE,INVOKE,READ | [] | 262144 |
| 24405 | Python | apo_gateway | openapi_tool_slack | TOOL | OBSERVE,INVOKE,READ | [8913] | 7258112 |
| 24407 | Python | apo_gateway | openapi_tool_google_pse | TOOL | OBSERVE,INVOKE,READ | [8914] | 6701056 |
| 24641 | bash | hyperai | apo_gateway | PROVIDER | OBSERVE,INVOKE,READ | [] | 278528 |
| 24643 | Python | hyperai | apo_gateway | PROVIDER | OBSERVE,INVOKE,READ | [9011] | 7290880 |
| 28463 | bash | apo_gateway | openapi_tool_external_rag | TOOL | OBSERVE,INVOKE,READ | [] | 278528 |
| 28465 | Python | apo_gateway | openapi_tool_external_rag | TOOL | OBSERVE,INVOKE,READ | [8912] | 10158080 |
| 28475 | Python | apo_gateway | openapi_tool_external_rag | TOOL | OBSERVE,INVOKE,READ | [] | 1114112 |
| 29817 | bash | hyperai | agent_os_dashboard | WORKER | OBSERVE,READ,WRITE | [] | 278528 |
| 29819 | Python | hyperai | agent_os_dashboard | WORKER | OBSERVE,READ,WRITE | [8777] | 6504448 |
| 35827 | ChatGPT for Chrome | codex | codex_operator_runtime | WORKER | OBSERVE,READ,WRITE | [] | 1998848 |
| 37164 | com.docker.virtualization | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 10813440 |
| 37180 | Docker Desktop | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 74088448 |
| 37186 | chrome_crashpad_handler | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 1736704 |
| 37193 | Docker Desktop Helper | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 11288576 |
| 37199 | Docker Desktop Helper | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 8077312 |
| 37265 | Docker Desktop Helper (Renderer) | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 108216320 |
| 37293 | docker-agent | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 4358144 |
| 37293 | docker-agent | docker | docker_desktop | INFRA | OBSERVE,ALLOCATE,EXECUTE | [] | 4358144 |
| 39662 | Python | hyperai_credentials | credential_broker | BROKER | OBSERVE,AUTH,VERIFY | [8765] | 7815168 |
| 39718 | Python | apo_gateway | openapi_tool_time | TOOL | OBSERVE,INVOKE,READ | [8901] | 6520832 |
| 39719 | Python | apo_gateway | openapi_tool_weather | TOOL | OBSERVE,INVOKE,READ | [8902] | 7602176 |
| 39720 | Python | apo_gateway | openapi_tool_filesystem | TOOL | OBSERVE,INVOKE,READ | [8903] | 6553600 |
| 39721 | Python | apo_gateway | openapi_tool_git | TOOL | OBSERVE,INVOKE,READ | [8904] | 6635520 |
| 39722 | Python | apo_gateway | openapi_tool_memory | TOOL | OBSERVE,INVOKE,READ | [8905] | 6537216 |
| 51004 | Bionic | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [1235, 52993] | 51167232 |
| 51004 | Bionic | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [1235, 52993] | 51167232 |
| 51007 | chrome_crashpad_handler | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 1802240 |
| 51007 | chrome_crashpad_handler | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [] | 1802240 |
| 51010 | Bionic Helper | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 11665408 |
| 51010 | Bionic Helper | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [] | 11665408 |
| 51011 | Bionic Helper | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 7225344 |
| 51011 | Bionic Helper | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [] | 7225344 |
| 51016 | node | apo_gateway | apo_upstream_lmstudio | PROVIDER | OBSERVE,INVOKE,READ | [] | 19906560 |
| 51016 | node | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 19906560 |
| 51016 | node | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [] | 19906560 |
| 51072 | Bionic Helper (Renderer) | apo_gateway | apo_upstream_lmstudio | PROVIDER | OBSERVE,INVOKE,READ | [] | 9453568 |
| 51072 | Bionic Helper (Renderer) | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 9453568 |
| 51072 | Bionic Helper (Renderer) | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [] | 9453568 |
| 51110 | lmlink-connector | apo_gateway | apo_upstream_lmstudio | PROVIDER | OBSERVE,INVOKE,READ | [42349] | 21086208 |
| 51110 | lmlink-connector | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [42349] | 21086208 |
| 52858 | node | apo_gateway | apo_upstream_lmstudio | PROVIDER | OBSERVE,INVOKE,READ | [] | 16678912 |
| 52858 | node | lmstudio | lmstudio_bionic_api | PROVIDER | OBSERVE,INVOKE,READ | [] | 16678912 |
| 52858 | node | element_labs | bionic_app | WORKER | OBSERVE,READ,WRITE | [] | 16678912 |
| 63375 | Python | aios | aios_mission_router | ROOT | OBSERVE,PLAN,ROUTE,VERIFY,AUTH,ALLOCATE,REVOKE | [9001] | 4063232 |
| 71954 | bash | hyperai | agent_os_dashboard | WORKER | OBSERVE,READ,WRITE | [] | 4472832 |
| 71954 | bash | aios | federation_orchestrator | ORCHESTRATOR | OBSERVE,PLAN,ROUTE,VERIFY | [] | 4472832 |
| 10064 | devin | redis | redis_local | MEMORY | OBSERVE,READ,WRITE | [] | 251281408 |

## 3. Phân loại Native / DAIOF / Unknown
- **Native (29)**: process thuộc ứng dụng macOS/ứng dụng độc lập, chưa có node DAIOF tương ứng hoặc đang chạy nền.
  - `526` ControlCenter
  - `2779` Antigravity IDE Helper (Plugin)
  - `3557` Antigravity IDE Helper (Plugin)
  - `3612` Python
  - `4812` Python
  - `4813` Python
  - `32831` Python
  - `37050` com.docker.backend
  - `37054` com.docker.backend
  - `37055` com.docker.backend
  - `37163` com.docker.build
  - `61565` intelligencecontextd
  - `70684` modelcatalogd
  - `71955` Python
  - `640` Spotlight
  - `1155` Electron
  - `1169` LM Studio
  - `2156` LM Studio Helper (GPU)
  - `2183` Antigravity IDE Helper (Plugin)
  - `2206` Antigravity IDE Helper
  - `2359` Antigravity IDE Helper
  - `2582` language_server_macos_arm
  - `2691` remoting_me2me_host
  - `3642` Python
  - `3704` LM Studio Helper
- **DAIOF projection (58)**: process đã được ánh xạ sang node trong registry, có role/authority xác định.
- **Unknown (16)**: process không khớp registry và không rõ vai trò.
  - `323` com.docker.vmnet
  - `2617` zsh
  - `2700` node
  - `2707` node
  - `2708` node
  - `10069` node
  - `10079` node
  - `10177` node
  - `10195` node
  - `10207` node
  - `62104` SAExtensionOrchestrator
  - `70688` generativeexperiencesd
  - `70715` ModelCatalogAgent
  - `1` launchd
  - `4594` node
  - `10078` node

## 4. Phân tích per app/runtime
| id | role | owner | capability | authority | auth | resources | value | state |
|---|---|---|---|---|---|---|---|---|
| apo_upstream_macbook_ollama | PROVIDER | apo_gateway | provider | OBSERVE INVOKE READ | none | rss=25001984 ports=[11434, 49196] | launchd_or_daemon | qualified |
| apo_upstream_titan_ollama | PROVIDER | apo_gateway | provider | OBSERVE INVOKE READ | none | rss=25001984 ports=[11434, 49196] | launchd_or_daemon | qualified |
| apo_upstream_macmini_ollama | PROVIDER | apo_gateway | provider | OBSERVE INVOKE READ | none | rss=25001984 ports=[11434, 49196] | launchd_or_daemon | qualified |
| apo_upstream_lmstudio | PROVIDER | apo_gateway | provider | OBSERVE INVOKE READ | LMSTUDIO_API_KEY:PRESENT | rss=100630528 ports=[42349, 50588] | process_group | qualified |
| openapi_tool_time | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6520832 ports=[8901] | process_group | qualified |
| openapi_tool_weather | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=7602176 ports=[8902] | process_group | qualified |
| openapi_tool_filesystem | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6553600 ports=[8903] | process_group | qualified |
| openapi_tool_git | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6635520 ports=[8904] | process_group | qualified |
| openapi_tool_memory | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6537216 ports=[8905] | process_group | qualified |
| openapi_tool_quotes | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6864896 ports=[8906] | process_group | qualified |
| openapi_tool_flashcards | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6946816 ports=[8907] | process_group | qualified |
| openapi_tool_time_ui | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6914048 ports=[8908] | process_group | qualified |
| openapi_tool_summarizer | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=7651328 ports=[8909] | process_group | qualified |
| openapi_tool_bitcoin | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=6930432 ports=[8910] | process_group | qualified |
| openapi_tool_sql | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | DATABASE_URL:PRESENT; OPENAI_API_KEY:PRESENT | rss=7602176 ports=[8911] | process_group | qualified |
| openapi_tool_external_rag | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | none | rss=11550720 ports=[8912] | process_group | qualified |
| openapi_tool_slack | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | SLACK_BOT_TOKEN:MISSING; SLACK_TEAM_ID:MISSING | rss=7782400 ports=[8913] | process_group | NOT qualified: auth:SLACK_BOT_TOKEN,auth:SLACK_TEAM_ID |
| openapi_tool_google_pse | TOOL | apo_gateway | openapi tool server | OBSERVE INVOKE READ | GOOGLE_API_KEY:PRESENT; GOOGLE_PSE_CX:MISSING | rss=7225344 ports=[8914] | process_group | NOT qualified: auth:GOOGLE_PSE_CX |
| mcp_pieces | MCP | apo_gateway | mcp server | OBSERVE INVOKE READ | token (path parameter):PRESENT_UNKNOWN | rss=244432896 ports=[39300, 52140] | launchd_or_daemon | qualified |
| mcp_docker_mcp | MCP | apo_gateway | mcp server | OBSERVE INVOKE READ | none | rss=0 ports=[] | manual_or_recycle | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| credential_broker | BROKER | hyperai_credentials | http service | OBSERVE AUTH VERIFY | none | rss=7815168 ports=[8765] | process_group | qualified |
| apo_gateway | PROVIDER | hyperai | http service | OBSERVE INVOKE READ | none | rss=7569408 ports=[9011] | process_group | qualified |
| agent_os_dashboard | WORKER | hyperai | http service | OBSERVE READ WRITE | none | rss=11255808 ports=[8777] | none | qualified |
| lmstudio_bionic_api | PROVIDER | lmstudio | openai compatible server | OBSERVE INVOKE READ | LMSTUDIO_API_KEY:PRESENT | rss=176848896 ports=[1235, 42349, 50588, 52993] | process_group | qualified |
| bionic_app | WORKER | element_labs | desktop electron runtime | OBSERVE READ WRITE | none | rss=117899264 ports=[1235, 52993] | none | qualified |
| ollama_macbook | PROVIDER | ollama | model substrate | OBSERVE INVOKE READ | none | rss=25001984 ports=[11434, 49196] | launchd_or_daemon | qualified |
| pieces_mcp | MCP | pieces | mcp server | OBSERVE INVOKE READ | none | rss=244432896 ports=[39300, 52140] | launchd_or_daemon | qualified |
| finalai | PROVIDER | finalai | http service | OBSERVE INVOKE READ | none | rss=3964928 ports=[50520] | launchd_or_daemon | qualified |
| redis_local | MEMORY | redis | cache store | OBSERVE READ WRITE | none | rss=259719168 ports=[6379, 50520] | none | qualified |
| hyperai_product_runtime | PRODUCT | hyperai-user-control-system | app runtime | OBSERVE READ WRITE EXECUTE | none | rss=0 ports=[] | manual_or_recycle | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| docker_desktop | INFRA | docker | container fabric | OBSERVE ALLOCATE EXECUTE | none | rss=218578944 ports=[] | none | qualified |
| federation_orchestrator | ORCHESTRATOR | aios | registry | OBSERVE PLAN ROUTE VERIFY | none | rss=4472832 ports=[] | none | qualified |
| memory_writer | MEMORY | aios | service runtime | OBSERVE READ WRITE | none | rss=0 ports=[] | manual_or_recycle | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| codex_operator_runtime | WORKER | codex | desktop operator runtime | OBSERVE READ WRITE | none | rss=1998848 ports=[] | none | qualified |
| aios_mission_router | ROOT | aios | service runtime | OBSERVE PLAN ROUTE VERIFY AUTH ALLOCATE REVOKE | none | rss=4063232 ports=[9001] | launchd_or_daemon | qualified |

## 5. Auth gap & khôi phục
| surface | key | status | source | refresh_path | consent_boundary |
|---|---|---|---|---|---|
| apo_upstream_anthropic | ANTHROPIC_API_KEY | MISSING | not found in known credential sources | credential_broker / ANTHROPIC_API_KEY | external paid API |
| apo_upstream_github_models | GITHUB_MODELS_TOKEN | MISSING | not found in known credential sources | credential_broker / GITHUB_MODELS_TOKEN | external paid API |
| apo_upstream_microsoftfoundry | AZURE_OPENAI_API_KEY | MISSING | not found in known credential sources | credential_broker / AZURE_OPENAI_API_KEY | external paid API |
| openapi_tool_slack | SLACK_BOT_TOKEN | MISSING | expected in credentials.env or keychain | credential_broker / SLACK_BOT_TOKEN | external account |
| openapi_tool_slack | SLACK_TEAM_ID | MISSING | not found in known credential sources | credential_broker / SLACK_TEAM_ID | external account |
| openapi_tool_google_pse | GOOGLE_PSE_CX | MISSING | expected in credentials.env or keychain | credential_broker / GOOGLE_PSE_CX | external account |
| mcp_pieces | token (path parameter) | PRESENT_UNKNOWN | SSE URL token param | Pieces app re-authentication | Pieces account |

### Khuyến nghị ưu tiên
1. `openapi_tool_slack`: cần `SLACK_BOT_TOKEN` và `SLACK_TEAM_ID` để Slack integration hoạt động. Nhập vào `~/.config/hyperai/credentials.env` hoặc keychain.
2. `openapi_tool_google_pse`: cần `GOOGLE_PSE_CX` (Programmable Search Engine ID). `GOOGLE_API_KEY` đã có trong `~/.zshrc`.
3. `apo_upstream_anthropic`/`github_models`/`microsoftfoundry`: keys thiếu nếu cần fallback inference. Nhưng chúng chưa cản trở qualified core.

## 6. Thứ tự binding / gate
Dựa trên `dependency_graph.json` và `binding_plan.json`:
1. **ROOT**: `aios_mission_router` đã chạy (port 9001), không phụ thuộc.
2. **INFRA**: `docker_desktop` và `redis_local` cần lên trước để các service có network/memory.
3. **BROKER / AUTH**: `credential_broker` (port 8765) cung cấp key lease.
4. **PROVIDER**: `ollama_macbook`, `apo_upstream_lmstudio`, `lmstudio_bionic_api`, `finalai` cung cấp inference.
5. **TOOL / MCP**: `openapi_tool_*` (ports 8901-8912), `mcp_pieces`, `pieces_mcp`, `mcp_docker_mcp` (cần khởi động port 8811).
6. **WORKER / PRODUCT**: `bionic_app`, `agent_os_dashboard`, `codex_operator_runtime`, `hyperai_product_runtime` (product cần recycle), `memory_writer`.
7. **ORCHESTRATOR**: `federation_orchestrator` chạy từ `runtime/federation_orchestrator/` (đã nhận diện chính script đang chạy).

### Blocker
- `mcp_docker_mcp` chưa lắng nghe port 8811 (`mcp_docker_mcp:8811 not started`).
- `hyperai_product_runtime` chưa có process tương ứng.
- `memory_writer` chỉ là script; cần một service runtime cố định hoặc lifecycle hook.

## 7. Ba bước tiếp theo
### immediate (trong phiên này)
- Cung cấp `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID`, `GOOGLE_PSE_CX` cho `credential_broker` hoặc `~/.config/hyperai/credentials.env`.
- Kiểm tra `mcp_docker_mcp`: khởi động MCP Docker SSE trên port 8811 nếu là gate có chủ đích.
### next (sau khi auth đủ)
- Chạy health probe trên toàn bộ qualified node, xác nhận từng `/health` trả về 200.
- Re-run qualifier sau khi `hyperai_product_runtime` / `memory_writer` được triển khai hoặc xóa khỏi mandatory list.
### pass condition (mở gate 2)
- 35/35 node qualified; không còn `MISSING` auth; `mcp_docker_mcp:8811` reachable; no plaintext secrets; invariants vẫn đúng.