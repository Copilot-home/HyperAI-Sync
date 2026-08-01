# ECOSYSTEM FLOW ANALYSIS
*Ngày: 2026-07-30T23:04:10.759330+00:00*
*Qualifier: 29/35 qualified*

## Lưu ý bảo mật
Trong quá trình đọc lại, phát hiện `runtime_discovery_snapshot.json` cũ chứa plaintext token (`OPENAI_API_KEY_3`) do regex mask không bắt định dạng `sk-proj-...`. Đã sửa regex trong `aios_runtime_qualification.py` và `verify_generated_artifacts.py`, re-run qualifier, verify pass, snapshot hiện tại không còn plaintext. Tuy nhiên, token đã bị lộ qua log/tool output trước đó; cần rotate khóa đó ở OpenAI dashboard.

## A. Trả lời 10 câu hỏi cho từng surface

| id | base_app | ai_projection | served_ecosystem | capability | value_flow_role | authority | auth_identity | auth_source | compute | state |
|---|---|---|---|---|---|---|---|---|---|---|
| apo_upstream_macbook_ollama | http://127.0.0.1:11434/v1 | apo_upstream_macbook_ollama (PROVIDER) | apo_gateway | provider | knowledge | OBSERVE INVOKE READ | none | none | rss=23855104 ports=[11434, 49196] pids=3 | qualified |
| apo_upstream_titan_ollama | http://192.168.3.84:11434/v1 | apo_upstream_titan_ollama (PROVIDER) | apo_gateway | provider | knowledge | OBSERVE INVOKE READ | none | none | rss=23855104 ports=[11434, 49196] pids=3 | qualified |
| apo_upstream_macmini_ollama | http://192.168.3.28:11434/v1 | apo_upstream_macmini_ollama (PROVIDER) | apo_gateway | provider | knowledge | OBSERVE INVOKE READ | none | none | rss=23855104 ports=[11434, 49196] pids=3 | qualified |
| apo_upstream_lmstudio | http://127.0.0.1:1235/v1 | apo_upstream_lmstudio (PROVIDER) | apo_gateway | provider | knowledge | OBSERVE INVOKE READ | LMSTUDIO_API_KEY:PRESENT | /Users/andy/.config/hyperai/credentials.env | rss=94781440 ports=[42349, 50588] pids=6 | qualified |
| openapi_tool_time | http://127.0.0.1:8901 | openapi_tool_time (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6520832 ports=[8901] pids=1 | qualified |
| openapi_tool_weather | http://127.0.0.1:8902 | openapi_tool_weather (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=7602176 ports=[8902] pids=1 | qualified |
| openapi_tool_filesystem | http://127.0.0.1:8903 | openapi_tool_filesystem (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6553600 ports=[8903] pids=1 | qualified |
| openapi_tool_git | http://127.0.0.1:8904 | openapi_tool_git (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6635520 ports=[8904] pids=1 | qualified |
| openapi_tool_memory | http://127.0.0.1:8905 | openapi_tool_memory (TOOL) | apo_gateway | openapi tool server | memory | OBSERVE INVOKE READ | none | none | rss=6537216 ports=[8905] pids=1 | qualified |
| openapi_tool_quotes | http://127.0.0.1:8906 | openapi_tool_quotes (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6864896 ports=[8906] pids=2 | qualified |
| openapi_tool_flashcards | http://127.0.0.1:8907 | openapi_tool_flashcards (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6946816 ports=[8907] pids=2 | qualified |
| openapi_tool_time_ui | http://127.0.0.1:8908 | openapi_tool_time_ui (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6914048 ports=[8908] pids=2 | qualified |
| openapi_tool_summarizer | http://127.0.0.1:8909 | openapi_tool_summarizer (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=7651328 ports=[8909] pids=2 | qualified |
| openapi_tool_bitcoin | http://127.0.0.1:8910 | openapi_tool_bitcoin (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=6930432 ports=[8910] pids=2 | qualified |
| openapi_tool_sql | http://127.0.0.1:8911 | openapi_tool_sql (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | DATABASE_URL:PRESENT; OPENAI_API_KEY:PRESENT | /Users/andy/.config/hyperai/credentials.env | rss=7602176 ports=[8911] pids=2 | qualified |
| openapi_tool_external_rag | http://127.0.0.1:8912 | openapi_tool_external_rag (TOOL) | apo_gateway | openapi tool server | execution | OBSERVE INVOKE READ | none | none | rss=11485184 ports=[8912] pids=3 | qualified |
| openapi_tool_slack | http://127.0.0.1:8913 | openapi_tool_slack (TOOL) | apo_gateway | openapi tool server | communication | OBSERVE INVOKE READ | SLACK_BOT_TOKEN:MISSING; SLACK_TEAM_ID:MISSING | expected in credentials.env or keychain; not found in known credential sources | rss=7782400 ports=[8913] pids=3 | NOT qualified: auth:SLACK_BOT_TOKEN,auth:SLACK_TEAM_ID |
| openapi_tool_google_pse | http://127.0.0.1:8914 | openapi_tool_google_pse (TOOL) | apo_gateway | openapi tool server | knowledge | OBSERVE INVOKE READ | GOOGLE_API_KEY:PRESENT; GOOGLE_PSE_CX:MISSING | expected in credentials.env or keychain; /Users/andy/.zshrc | rss=7225344 ports=[8914] pids=3 | NOT qualified: auth:GOOGLE_PSE_CX |
| mcp_pieces | http://127.0.0.1:39300 | mcp_pieces (MCP) | apo_gateway | mcp server | execution | OBSERVE INVOKE READ | token (path parameter):PRESENT_UNKNOWN | SSE URL token param | rss=232144896 ports=[39300, 52140] pids=2 | qualified |
| mcp_docker_mcp | http://127.0.0.1:8811 | mcp_docker_mcp (MCP) | apo_gateway | mcp server | execution | OBSERVE INVOKE READ | none | none | rss=0 ports=[] pids=0 | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| credential_broker | http://127.0.0.1:8765 | credential_broker (BROKER) | hyperai_credentials | http service | auth | OBSERVE AUTH VERIFY | none | none | rss=8224768 ports=[8765] pids=1 | qualified |
| apo_gateway | http://127.0.0.1:9011 | apo_gateway (PROVIDER) | hyperai | http service | routing | OBSERVE INVOKE READ | none | none | rss=7569408 ports=[9011] pids=2 | qualified |
| agent_os_dashboard | http://127.0.0.1:8777 | agent_os_dashboard (WORKER) | hyperai | http service | planning | OBSERVE READ WRITE | none | none | rss=6782976 ports=[8777] pids=2 | qualified |
| lmstudio_bionic_api | http://127.0.0.1:1235/v1 | lmstudio_bionic_api (PROVIDER) | lmstudio | openai compatible server | knowledge | OBSERVE INVOKE READ | LMSTUDIO_API_KEY:PRESENT | /Users/andy/.config/hyperai/credentials.env | rss=174260224 ports=[1235, 42349, 50588, 52993] pids=11 | qualified |
| bionic_app | http://127.0.0.1:52993 | bionic_app (WORKER) | element_labs | desktop electron runtime | execution | OBSERVE READ WRITE | none | none | rss=117751808 ports=[1235, 52993] pids=7 | qualified |
| ollama_macbook | http://127.0.0.1:11434 | ollama_macbook (PROVIDER) | ollama | model substrate | knowledge | OBSERVE INVOKE READ | none | none | rss=23855104 ports=[11434, 49196] pids=3 | qualified |
| pieces_mcp | http://127.0.0.1:39300 | pieces_mcp (MCP) | pieces | mcp server | execution | OBSERVE INVOKE READ | none | none | rss=232144896 ports=[39300, 52140] pids=2 | qualified |
| finalai | http://127.0.0.1:50520 | finalai (PROVIDER) | finalai | http service | knowledge | OBSERVE INVOKE READ | none | none | rss=3964928 ports=[50520] pids=1 | qualified |
| redis_local | redis://127.0.0.1:6379 | redis_local (MEMORY) | redis | cache store | memory | OBSERVE READ WRITE | none | none | rss=260833280 ports=[6379, 50520] pids=4 | qualified |
| hyperai_product_runtime | http://127.0.0.1:5000 | hyperai_product_runtime (PRODUCT) | hyperai-user-control-system | app runtime | product | OBSERVE READ WRITE EXECUTE | none | none | rss=0 ports=[] pids=0 | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| docker_desktop | container_fabric | docker_desktop (INFRA) | docker | container fabric | infrastructure | OBSERVE ALLOCATE EXECUTE | none | none | rss=174112768 ports=[] pids=7 | qualified |
| federation_orchestrator | registry | federation_orchestrator (ORCHESTRATOR) | aios | registry | planning | OBSERVE PLAN ROUTE VERIFY | none | none | rss=0 ports=[] pids=0 | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| memory_writer | service_runtime | memory_writer (MEMORY) | aios | service runtime | memory | OBSERVE READ WRITE | none | none | rss=0 ports=[] pids=0 | NOT qualified: observed_runtime,role_resolved,authority_resolved,dependencies_resolved,health_probed |
| codex_operator_runtime | desktop_operator_runtime | codex_operator_runtime (WORKER) | codex | desktop operator runtime | execution | OBSERVE READ WRITE | none | none | rss=2473984 ports=[] pids=1 | qualified |
| aios_mission_router | service_runtime | aios_mission_router (ROOT) | aios | service runtime | routing | OBSERVE PLAN ROUTE VERIFY AUTH ALLOCATE REVOKE | none | none | rss=4063232 ports=[9001] pids=1 | qualified |

## B. Auth Mastery
Bảng dưới tổng hợp từ `auth_topology.json` và live broker `/status`.

| surface | key | account/workspace | provider | scope | credential_ref | status | source | refresh_path | consent_boundary | recovery_path |
|---|---|---|---|---|---|---|---|---|---|---|
| apo_upstream_openai | OPENAI_API_KEY |  | openai | model inference | credential_broker / OPENAI_API_KEY | PRESENT | /Users/andy/.config/hyperai/credentials.env | credential_broker / OPENAI_API_KEY | external paid API |  |
| apo_upstream_anthropic | ANTHROPIC_API_KEY |  | anthropic | model inference | credential_broker / ANTHROPIC_API_KEY | MISSING | not found in known credential sources | credential_broker / ANTHROPIC_API_KEY | external paid API | Thêm ANTHROPIC_API_KEY nếu cần fallback; hoặc dùng OpenAI/OpenRouter |
| apo_upstream_openrouter | OPENROUTER_API_KEY |  | openrouter | model inference | credential_broker / OPENROUTER_API_KEY | PRESENT | /Users/andy/.config/hyperai/credentials.env | credential_broker / OPENROUTER_API_KEY | external paid API |  |
| apo_upstream_google | GEMINI_API_KEY |  | google | model inference | credential_broker / GEMINI_API_KEY | PRESENT | /Users/andy/.zshrc | credential_broker / GEMINI_API_KEY | external paid API |  |
| apo_upstream_github_models | GITHUB_MODELS_TOKEN |  | github_models | model inference | credential_broker / GITHUB_MODELS_TOKEN | MISSING | not found in known credential sources | credential_broker / GITHUB_MODELS_TOKEN | external paid API | Thêm GITHUB_MODELS_TOKEN nếu cần GitHub Models; GITHUB_PAT hiện đang dùng cho github provider |
| apo_upstream_microsoftfoundry | AZURE_OPENAI_API_KEY |  | microsoftfoundry | model inference | credential_broker / AZURE_OPENAI_API_KEY | MISSING | not found in known credential sources | credential_broker / AZURE_OPENAI_API_KEY | external paid API | Thêm AZURE_OPENAI_API_KEY nếu cần Azure Foundry |
| apo_upstream_lmstudio | LMSTUDIO_API_KEY |  | lmstudio | model inference | credential_broker / LMSTUDIO_API_KEY | PRESENT | /Users/andy/.config/hyperai/credentials.env | credential_broker / LMSTUDIO_API_KEY | external paid API |  |
| openapi_tool_slack | SLACK_BOT_TOKEN |  | Slack workspace | tool:slack | credential_broker / SLACK_BOT_TOKEN | MISSING | expected in credentials.env or keychain | credential_broker / SLACK_BOT_TOKEN | external account | Tạo Slack app -> OAuth consent -> install bot -> broker load SLACK_BOT_TOKEN; team_id từ auth.test/workspace URL |
| openapi_tool_slack | SLACK_TEAM_ID |  | Slack workspace | tool:slack | credential_broker / SLACK_TEAM_ID | MISSING | not found in known credential sources | credential_broker / SLACK_TEAM_ID | external account | Tạo Slack app -> OAuth consent -> install bot -> broker load SLACK_BOT_TOKEN; team_id từ auth.test/workspace URL |
| openapi_tool_google_pse | GOOGLE_API_KEY |  | Google Programmable Search | tool:google_pse | credential_broker / GOOGLE_API_KEY | PRESENT | /Users/andy/.zshrc | credential_broker / GOOGLE_API_KEY | external account |  |
| openapi_tool_google_pse | GOOGLE_PSE_CX |  | Google Programmable Search | tool:google_pse | credential_broker / GOOGLE_PSE_CX | MISSING | expected in credentials.env or keychain | credential_broker / GOOGLE_PSE_CX | external account | Tạo Google Programmable Search Engine -> lấy CSE ID -> lưu GOOGLE_PSE_CX; GOOGLE_API_KEY đã có |
| openapi_tool_sql | DATABASE_URL |  | SQL database + OpenAI | tool:sql | credential_broker / DATABASE_URL | PRESENT | /Users/andy/.config/hyperai/credentials.env | credential_broker / DATABASE_URL | local database |  |
| openapi_tool_sql | OPENAI_API_KEY |  | SQL database + OpenAI | tool:sql | credential_broker / OPENAI_API_KEY | PRESENT | /Users/andy/.config/hyperai/credentials.env | credential_broker / OPENAI_API_KEY | local database |  |
| mcp_pieces | token (path parameter) |  | Pieces | mcp bridge | Pieces app re-authentication | PRESENT_UNKNOWN | SSE URL token param | Pieces app re-authentication | Pieces account |  |
| lmstudio_bionic_api | LMSTUDIO_API_KEY |  | LM Studio | local inference | LM Studio app settings | PRESENT | /Users/andy/.config/hyperai/credentials.env | LM Studio app settings | local app |  |

## C. Role Mastery — Lane
### lane: routing
- nodes: aios_mission_router, apo_gateway
- input: request
- output: routed call
- upstream: clients
- downstream: providers/tools
- authority: OBSERVE ROUTE
- compute cost: gateway
- value contribution: service integration
- failure impact: routing down

### lane: planning
- nodes: federation_orchestrator, agent_os_dashboard
- input: mission / query
- output: plan / route decision
- upstream: creator, router
- downstream: execution lane
- authority: OBSERVE PLAN ROUTE
- compute cost: route compute
- value contribution: correct routing
- failure impact: wrong route

### lane: auth
- nodes: credential_broker
- input: key request
- output: scoped lease
- upstream: credentials.env / keychain
- downstream: execution lane
- authority: AUTH VERIFY
- compute cost: broker
- value contribution: secure identity
- failure impact: unauthorized

### lane: knowledge
- nodes: apo_upstream_macbook_ollama, apo_upstream_titan_ollama, apo_upstream_macmini_ollama, apo_upstream_lmstudio, ollama_macbook, lmstudio_bionic_api, finalai, openapi_tool_google_pse
- input: queries / prompts
- output: model responses / search results
- upstream: providers
- downstream: tools/router
- authority: OBSERVE INVOKE READ
- compute cost: model inference / search
- value contribution: inference value
- failure impact: LLM/search unavailable

### lane: memory
- nodes: redis_local, memory_writer, openapi_tool_memory
- input: write / read
- output: stored state
- upstream: all lanes
- downstream: all lanes
- authority: OBSERVE READ WRITE
- compute cost: redis/disk
- value contribution: continuity
- failure impact: state loss

### lane: execution
- nodes: mcp_pieces, pieces_mcp, mcp_docker_mcp, openapi_tool_time, openapi_tool_weather, openapi_tool_filesystem, openapi_tool_git, openapi_tool_quotes, openapi_tool_flashcards, openapi_tool_time_ui, openapi_tool_summarizer, openapi_tool_bitcoin, openapi_tool_sql, openapi_tool_external_rag, bionic_app, codex_operator_runtime
- input: tool call / task
- output: tool result
- upstream: router
- downstream: product/memory
- authority: OBSERVE INVOKE READ WRITE
- compute cost: tool process
- value contribution: task completion
- failure impact: tool fails

### lane: communication
- nodes: openapi_tool_slack
- input: messages / mentions
- output: sent messages / reactions
- upstream: Slack workspace
- downstream: tools/router
- authority: OBSERVE INVOKE READ
- compute cost: Slack API calls
- value contribution: team coordination
- failure impact: Slack unreachable

### lane: product
- nodes: hyperai_product_runtime
- input: user action
- output: UI state
- upstream: runtime
- downstream: backend
- authority: OBSERVE READ WRITE EXECUTE
- compute cost: browser/frontend
- value contribution: user value
- failure impact: product not running

### lane: infrastructure
- nodes: docker_desktop
- input: container / net request
- output: network / vm
- upstream: OS
- downstream: all
- authority: OBSERVE ALLOCATE EXECUTE
- compute cost: Docker daemon
- value contribution: runtime fabric
- failure impact: Docker down

## D. Host Topology
- **MacBook** = ACTIVE_CONTROL_HOST: tất cả process hiện đang chạy (103 process), tất cả ports 127.0.0.1 và local model substrate.
- **Titan** = MAINTENANCE_STANDBY_HOST: `apo_config.yaml` định nghĩa `titan_ollama` tại `192.168.3.84:11434`; hiện không reachable, các alias `apo/code`, `apo/local-large` đang trỏ vào host không hoạt động.
- **MacMini** = STANDBY (nếu tồn tại): `macmini_ollama` tại `192.168.3.28:11434`, cũng không reachable.

### Registry nodes theo host
| node | host | lý do |
|---|---|---|
| apo_upstream_macbook_ollama | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| apo_upstream_titan_ollama | TITAN_STANDBY | base_url 192.168.3.84 / titan in id |
| apo_upstream_macmini_ollama | MACMINI_STANDBY | base_url 192.168.3.28 / macmini in id |
| apo_upstream_lmstudio | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_time | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_weather | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_filesystem | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_git | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_memory | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_quotes | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_flashcards | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_time_ui | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_summarizer | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_bitcoin | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_sql | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_external_rag | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_slack | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| openapi_tool_google_pse | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| mcp_pieces | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| mcp_docker_mcp | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| credential_broker | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| apo_gateway | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| agent_os_dashboard | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| lmstudio_bionic_api | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| bionic_app | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| ollama_macbook | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| pieces_mcp | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| finalai | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| redis_local | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| hyperai_product_runtime | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| docker_desktop | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| federation_orchestrator | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| memory_writer | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| codex_operator_runtime | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |
| aios_mission_router | MACBOOK_ACTIVE | local 127.0.0.1 hoặc process đang chạy trên MacBook |

## E. Ba đề xuất

### 1. Việc nên làm ngay — Resolve auth cho Slack và Google PSE
- **Evidence**: `auth_topology.json` ghi MISSING `SLACK_BOT_TOKEN`, `SLACK_TEAM_ID`, `GOOGLE_PSE_CX`; broker `/status` báo `slack` và `google_pse` `valid_key: null, healthy: false, tried: 0`; `credentials.env` có `GOOGLE_API_KEY` nhưng thiếu `GOOGLE_PSE_CX`; `hyperai_credentials_service.py` đã có proxy `/proxy/slack` và `/proxy/google_pse/search`.
- **Expected value**: Hai TOOL surface (`openapi_tool_slack`, `openapi_tool_google_pse`) trở thành qualified, mở kênh communication (Slack) và web search (PSE) cho hệ sinh thái.
- **Compute cost**: thấp — chỉ thêm validation call khi broker khởi động và khi có request.
- **Risk**: quota Slack/Google API; cần consent đúng scope, không paste plaintext secret.
- **Required authority**: BROKER (credential_broker / 8765) + Creator consent để tạo Slack app / CSE.
- **PASS condition**: broker `/status` hiển thị `slack` và `google_pse` `healthy: true`; `GET /health` trên cả hai server trả về 200; qualifier re-run cho 31+/35.

### 2. Việc nên làm kế tiếp — Reconcile upstream / host topology
- **Evidence**: `apo_config.yaml` định nghĩa `macbook_ollama` (127.0.0.1:11434), `titan_ollama` (192.168.3.84:11434), `macmini_ollama` (192.168.3.28:11434); `lsof` chỉ thấy port 11434 trên 127.0.0.1; cùng một process Ollama (PID 831/864) được ánh xạ cho cả 3 upstream.
- **Expected value**: Loại bỏ duplicate authority, rõ ràng MacBook là active substrate, Titan/macmini là standby; giảm sai lệch khi route alias `apo/code`, `apo/local-large`.
- **Compute cost**: trung bình — cần cập nhật registry hoặc `apo_config.yaml` để phân biệt reachable host.
- **Risk**: nếu Titan đột ngột online, route có thể bị trùng; cần giữ lineage và capability inventory.
- **Required authority**: ROOT/ORCHESTRATOR (aios_mission_router / federation_orchestrator).
- **PASS condition**: Chỉ một active Ollama provider trên MacBook; `titan_ollama` và `macmini_ollama` được đánh dấu STANDBY trong registry; alias `apo/code` và `apo/local-large` chuyển sang MacBook hoặc unavailable.

### 3. Việc nên làm sau đó — Qualify / classify 16 unknown process
- **Evidence**: `runtime_discovery_snapshot.json` có 16 process UNKNOWN (không khớp registry); trong đó có `mcp-proxy`, `get-oauth-tokens`, `get-tokens-from-cookies`, `get-user-info`, các `node` từ npx, dịch vụ hệ thống (`launchd`, `com.docker.vmnet`, `SAExtensionOrchestrator`, ...).
- **Expected value**: Mở rộng qualified surface, không để process vô danh; tận dụng các tool server đã có sẵn trong `openapi-servers/servers/` nhưng chưa registry.
- **Compute cost**: trung bình — cần thêm node registry hoặc gán lại role cho từng process.
- **Risk**: misclassify; một số process như `get-oauth-tokens` có thể là security surface cần giám sát đặc biệt.
- **Required authority**: ORCHESTRATOR + SECURITY REVIEW.
- **PASS condition**: Mỗi unknown process được gán một trong: NATIVE, DAIOF, hoặc SUPPRESSED; registry cập nhật; qualification count > 30.

## F. SOCRATIC VERIFICATION CYCLE

**QUESTIONS_ASKED**
1. Có đúng `apo_upstream_titan_ollama` và `apo_upstream_macmini_ollama` đang chạy trên các host riêng biệt không?
2. Tại sao cùng một process Ollama local lại được ánh xạ cho cả ba upstream?
3. Mô hình `apo/code` và `apo/local-large` đang định tuyến đến đâu trong thực tế?

**EVIDENCE_FOUND**
- Source: `apo_config.yaml` dòng 34-42: `macbook_ollama` -> 127.0.0.1:11434, `titan_ollama` -> 192.168.3.84:11434, `macmini_ollama` -> 192.168.3.28:11434.
- Process: `Ollama` (pid 831) và `ollama` (pid 864) listen trên 127.0.0.1:11434; `lsof -nP -iTCP:11434 -sTCP:LISTEN` chỉ trả về local.
- Registry: `runtime_registry.json` có 3 node Ollama; `binding_plan.json` gán cả 3 cùng PID 831/864.
- Config aliases: `apo/code` -> titan_ollama, `apo/local-large` -> titan_ollama, `apo/apple` -> macbook_ollama.

**VERIFIED_CONCLUSIONS**
- MacBook Ollama là substrate duy nhất đang active.
- Titan (192.168.3.84) và MacMini (192.168.3.28) không reachable từ MacBook hiện tại.
- Ba upstream node trong registry trỏ đến cùng một thực thể vật lý -> duplicate authority.

**NOT_PROVEN**
- Titan có đang bật và chỉ bị network partition hay đã tắt hoàn toàn.
- MacMini có tồn tại vật lý không.

**HISTORICAL_RECONCILIATION**
- Canon (`apo_config.yaml`) giả định 3 host Ollama. Physical reality hiện tại chỉ có 1. Đây là STATE_DRIFT do Titan ở maintenance standby / MacMini không reachable.

**CANON_DELTA**
- `titan_ollama`: DOWNGRADE to STANDBY projection.
- `macmini_ollama`: DOWNGRADE to STANDBY projection.
- `macbook_ollama`: RETAIN as ACTIVE.
- Aliases `apo/code`, `apo/local-large`: cần route fallback hoặc unavailable.

**DECISION**
- Quyết định: DOWNGRADE_CANON.
- Lý do: Physical reality chỉ có một active Ollama; giữ 3 node nhưng đánh dấu standby tránh duplicate authority.
- Confidence: cao.
- Next action: cập nhật `runtime_registry.json` hoặc `role_registry.json` với trạng thái STANDBY cho titan/macmini.

**NEXT_SOCRATIC_QUESTIONS**
1. Khi nào Titan sẽ quay lại và cần probe gì để kích hoạt lại `titan_ollama`?
2. Có nên giữ `macmini_ollama` trong registry hay loại bỏ hoàn toàn?
3. `apo/code` và `apo/local-large` nên fallback về MacBook hay báo unavailable?