# APO SUPERSYSTEM DISCOVERY REPORT

**Execution ID:** apo-supersystem-discovery-20260731  
**Scope:** CREATOR_HOME (`/Users/andy`) as SOURCE HABITAT + AI MEMORY SURFACE + RUNTIME SUBSTRATE + CAPABILITY RESERVOIR + RECOVERY DOMAIN  
**Timestamp:** 2026-07-31T14:15:00Z  
**Operator:** Devin under HyperAI Canon  
**Verdict:** `APO_SUPERSYSTEM_BOUND — SYSTEM_DISCOVERY_PARTIAL`

---

## I. PHÁN QUYẾT CAO NHẤT

`/Users/andy` không phải một ổ đĩa cần dọn. Nó là một **super-system** gồm 20+ actor đang hợp tác để tạo giá trị gộp lớn hơn tổng giá trị riêng lẻ. Hiện tại:

- **Core green chain** đã được xác minh: Ollama, FinalAI, **AIOS Runtime Orchestrator (Phoenix)**, Docker Desktop, agent_os, apo_gateway, 14 OpenAPI server, Redis.
- **Port 9001** thực chất là `/Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py`, không chỉ là một health bridge.
- **APO capability network** có 10 transport planes; 14 OpenAPI server chạy trên host uvicorn, **không chạy trong Docker**.
- **APO Gateway** đã làm unified router qua `/tools/{name}/{path}`; **credential broker** healthy với 9 active keys.
- **Một mission thực** đã được trace: `AIOS :9001 → APO :9011 → time :8901 → Devin → memory`.
- **Model fabric** gồm 4 store với nhiều format và duplicate.
- **OpenAPI home fabric** có 18 server, 14 đang live trên :8901-:8914; APO registry active, 4 dormant server ngoài registry.
- **Workbench source habitat** chứa aios_runtime_orchestrator, D&R Protocol, HyperAI Copilot Electron, Workbench Agent Orchestrator, Agent Data System.
- **Các trục GOVERNANCE, DATA, EXECUTION, LANGUAGE, VISION** đã có holder xác minh.
- **Các trục ECONOMICS, LOGIC, FORMAL_LOGIC** đang understaffed.
- **Port 5000** thuộc về macOS Control Center; không phải conflict chưa được giải quyết.
- **Drift:** `aios_mission_router.py` tham chiếu `~/.con-memory/conversations.db` và `~/.codex/config.toml` không tồn tại; `HyperAI-Sync`, `~/.codex/AGENTS.md`, `~/.agents/skills` tồn tại.

Hệ **không xây một siêu AI**. Hệ xây một nhóm anh em biết ai giỏi việc gì, ai chịu trách nhiệm gì, và cùng tạo lợi nhuận gộp.

---

## II. ONTOLOGY GỐC

Mỗi object trong `/Users/andy` chỉ có ý nghĩa khi biết nó nằm trên causal path nào:

```
source → build → registry → runtime → capability → mission → verified value → memory → recovery
```

Ví dụ:

- `~/.ollama` là **MODEL_WEIGHT** + **ACTIVE_RUNTIME_STATE** trên path `source (registry.ollama.ai) → runtime (ollama serve) → capability (local inference) → mission (Devin reasoning) → verified value (/api/tags 200) → memory (HyperAI-Sync) → recovery (restart Ollama.app)`.
- `~/docker-recovery/evidence-20260729` là **FAILURE_FOSSIL** trên path `failure (Docker.raw read-only) → recovery (retire redundant copies) → memory (fossil manifest) → future value (avoid same failure)`.

Không xem `storage size = value`. Value = capability dependency × runtime usage × lineage × recovery role.

---

## III. SUPER-SYSTEM ACTORS

| ID | Actor | Surface | Primary Axis | Responsibility Status | Runtime State |
|---|---|---|---|---|---|
| actor_001 | Ollama | `~/.ollama`, `:11434` | EXECUTION | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_002 | LM Studio | `~/.lmstudio`, `:1234` | EXECUTION | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_003 | Pieces OS | `~/Library/com.pieces.os`, `:39300` | DATA | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_004 | FinalAI Proxy | `~/.local/bin/finalai-openai-proxy.py`, `:50520` | GOVERNANCE | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_005 | AIOS Runtime Orchestrator (Phoenix) | `~/workbench/aios_runtime_orchestrator/aios_mission_router.py`, `:9001` | GOVERNANCE | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_006 | Docker Desktop | `/Applications/Docker.app`, `~/Library/Containers/com.docker.docker` | EXECUTION | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_007 | HyperAI Agent OS | `~/HyperAI/agent_os.py`, `:8777` | GOVERNANCE | AXIS_CANDIDATE | ACTIVE |
| actor_008 | APO Gateway | `~/.apo/gateway/apo_gateway.py`, `:9011` | GOVERNANCE | AXIS_CANDIDATE | ACTIVE |
| actor_009 | OpenAPI Home Fabric | `~/openapi-servers`, `:8901-8914` | EXECUTION | AXIS_CANDIDATE | ACTIVE |
| actor_010 | HyperAI OS Master | `~/workbench/hyperai_os_master.py` | GOVERNANCE | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_011 | HyperAI-Sync | `~/HyperAI-Sync` | DATA | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_012 | Antigravity IDE | `/Applications/Antigravity IDE.app`, `~/.antigravity-ide` | EXECUTION | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_013 | VS Code / Insiders | `~/.vscode`, `~/.vscode-insiders`, `~/Library/Application Support/Code*` | EXECUTION | AXIS_HOLDER_VERIFIED | DORMANT |
| actor_014 | VSCodium | `~/Library/Application Support/VSCodium` | EXECUTION | AXIS_HOLDER_VERIFIED | DORMANT |
| actor_015 | Devin / Devin CLI | `~/.local/share/devin`, `~/.devin` | GOVERNANCE | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_016 | Notion / Notion Mail | `~/Library/Application Support/Notion*` | DATA | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_017 | Pictures | `~/Pictures` | DATA | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_018 | Projects / AI Habitat | `~/projects` | CODE | AXIS_HOLDER_VERIFIED | DORMANT |
| actor_019 | Archive | `~/Archive` | DATA | AXIS_CANDIDATE | DORMANT |
| actor_020 | macOS Control Center | `:5000` | GOVERNANCE | OS_AUTHORITY | ACTIVE |
| actor_021 | Workbench Source Habitat | `/Users/andy/workbench` | CODE | AXIS_HOLDER_VERIFIED | ACTIVE |
| actor_022 | D&R Protocol | `/Users/andy/workbench/dr_protocol` | LOGIC / FORMAL_LOGIC | AXIS_CANDIDATE | DORMANT |
| actor_023 | HyperAI Copilot Electron | `/Users/andy/workbench/electron` | EXECUTION | AXIS_CANDIDATE | DORMANT |
| actor_024 | Workbench Agent Orchestrator | `/Users/andy/workbench/agents` | EXECUTION | AXIS_CANDIDATE | DORMANT |
| actor_025 | Agent Data System | `/Users/andy/workbench/.agent_data` | DATA | AXIS_CANDIDATE | DORMANT |
| actor_026 | Agent Broker | `/Users/andy/agent_broker.py` | SECURITY | AXIS_CANDIDATE | DORMANT |
| actor_027 | GKE MCP Server | `gke-mcp`, `:8080` | EXECUTION | AXIS_CANDIDATE | UNCERTAIN |
| actor_028 | DAIOF-Framework | `/Users/andy/DAIOF-Framework` | LOGIC / FORMAL_LOGIC | AXIS_CANDIDATE | DORMANT |

---

## IV. AXIS CAPABILITY RESPONSIBILITY MATRIX

| Trục | Holder chính | Co-holder | Gap / Trách nhiệm còn thiếu |
|---|---|---|---|
| LANGUAGE | Ollama | Pieces OS, Antigravity IDE | VS Code family có capability nhưng không active |
| LOGIC | null | OpenAPI fabric, DAIOF-Framework | DAIOF dormant; OpenAPI chưa có reasoning orchestration |
| FORMAL_LOGIC | null | DAIOF-Framework | Không có active formal-logic runtime |
| VISION | HyperAI-Sync | LM Studio, Antigravity IDE | Vẫn là static Canon, thiếu dynamic simulation |
| DATA | HyperAI-Sync + Pieces OS | Ollama, Redis, Notion, Agent Data System | Thiếu unified vector/semantic memory |
| EXECUTION | Docker + OpenAPI Home | Ollama, FinalAI, AIOS Runtime Orchestrator, Antigravity IDE, HyperAI Copilot Electron, Workbench Agent Orchestrator | Port sprawl; APO binding chưa xác minh |
| SECURITY | Docker + HyperAI-Sync | APO Gateway, Agent Broker | Credential service endpoint chưa rõ |
| ECONOMICS | null | - | **UNDERSTAFFED**: không ai chịu trách nhiệm compute/storage budget |
| GOVERNANCE | OS Master + HyperAI-Sync + Devin | Agent OS, APO Gateway, FinalAI, AIOS Runtime Orchestrator | Agent OS / APO chưa được chứng minh là primary |

---

## V. MODEL FABRIC

| Store | Path | Physical Size | Active Models | Dormant / Debt | Verdict |
|---|---|---|---|---|---|
| Ollama | `~/.ollama` | 17 GB | llama3.1:8b, all-minilm, chatgpt alias | gpt-5.5 alias, cloud refs | primary local inference |
| LM Studio | `~/.lmstudio` | 26 GB | 8 models (GGUF + MLX) | virtual LFM2.5, duplicate nomic-embed bundles | secondary GUI inference |
| AITK | `~/.aitk` | 2.3 GB | 0 | 4 DeepSeek 1.5B variants, incomplete 14B, Qwen 0.5B | dormant Azure Toolkit |
| Pieces OS | `~/Library/com.pieces.os` | 14 GB | 0 (cloud model) | snapshots, agentic traces | snippet/index memory, not weight store |

**Duplicate candidates:**
- `nomic-embed-text-v1.5` trong LM Studio: 4 bản copy (~800 MB).
- `DeepSeek R1 Distill Qwen 1.5B` trong AITK: 4 variants khác quantization/runtime (~2.4 GB).
- `Qwen 0.5B` trong cả LM Studio (MLX) và AITK (ONNX).

**Lineage chính:**
- Ollama dùng GGUF, là runtime được nhiều surface dùng nhất.
- LM Studio dùng MLX/GGUF, là GUI-driven fallback.
- AITK dùng ONNX, hiện dormant, targeted CPU/CUDA.
- Pieces không lưu weight; nó lưu snippet, chat, agentic traces.

---

## VI. OPENAPI HOME FABRIC

**18 servers, 14 live trên 8901-8914.**

| Port | Server | Capability | Axis | Trạng thái |
|---|---|---|---|---|
| 8901 | time | time | EXECUTION | LIVE |
| 8902 | weather | weather | EXECUTION | LIVE |
| 8903 | filesystem | filesystem | EXECUTION | LIVE |
| 8904 | git | git | EXECUTION | LIVE |
| 8905 | memory | memory (knowledge graph) | DATA | LIVE |
| 8906 | quotes-ui | UI rendering | EXECUTION | LIVE |
| 8907 | flashcards | UI rendering | EXECUTION | LIVE |
| 8908 | time-ui | UI rendering | EXECUTION | LIVE |
| 8909 | summarizer_tool | summarizer | LANGUAGE | LIVE |
| 8910 | bitcoin-price-predictor | financial analysis | LOGIC | LIVE |
| 8911 | sql | sql | DATA | LIVE |
| 8912 | external-rag | retrieval | DATA | LIVE |
| 8913 | slack | slack | EXECUTION | LIVE |
| 8914 | google-pse | web search | DATA | LIVE |
| 8000 (dormant) | auth x3, mcp-proxy | auth, mcp | SECURITY / EXECUTION | DORMANT |

**Friction chính:**
- APO Gateway đã có unified `tools` registry và proxy /tools/{name}/... hoạt động (verified qua /tools/time/openapi.json). Tuy nhiên, chưa có health/lease enforcement từng tool.
- summarizer có 2 directory (`summarizer-tool` vs `summarizer_tool`) và port mapping khác compose.
- 4 dormant server (auth x3, mcp-proxy) chưa được thêm vào APO tools registry.

---

## VII. PORT AUTHORITY MAP

| Port | Service | Authority | Health | Ghi chú |
|---|---|---|---|---|
| 9001 | AIOS Runtime Orchestrator (Phoenix) | HyperAI green baseline / GOVERNANCE | 200 | mission router + health bridge (PID 63375) |
| 50520 | FinalAI Proxy | HyperAI green baseline | 200 | OpenAI-compatible proxy |
| 11434 | Ollama | local model runtime | 200 | /api/tags OK |
| 8777 | Agent OS | HyperAI governance | 200 | /openapi.json OK |
| 9011 | APO Gateway | HyperAI governance | 200 | /health OK |
| 8901-8914 | OpenAPI Home | capability fabric | 200 openapi | 14 live |
| 6379 | Redis | utility plane | listening | |
| 10533 | Postman | utility | listening | |
| 8080 | code-server (likely; gke-mcp may also claim) | utility | listening | potential actor conflict: code-server PID 4624 vs GKE MCP Server expected on 8080 |
| 3001, 23333, 7779 | Antigravity IDE | active creator surface | listening | |
| 1234, 41343 | LM Studio | active model GUI | listening | |
| 39300, 50999 | Pieces OS | active snippet/AI | listening | |
| 5000 | macOS Control Center | OS authority | 403 | **NOT HyperAI backend** |

**Phán quyết port 5000:** `OS_RESERVED_PORT`. Không giết Control Center. HyperAI backend cần port khác hoặc config cũ cần được cập nhật.

---

## VIII. STORAGE CAPABILITY LINEAGE

| Class | Tổng GB | Vai trò | Có thể reclaim? |
|---|---|---|---|
| MODEL_WEIGHT | 71 | capability runtime | Không; cần audit duplicate trước |
| ACTIVE_PROJECT_DATA | 92.5 | app user state | Một phần cache/log |
| AUTHORITATIVE_USER_DATA | 9.3 | personal data | Không |
| CODE | 7.2 | source habitat | Không |
| FAILURE_FOSSIL | 5.1 | evidence/archive | Không (chưa) |
| RUNTIME | 8.7 | dev tools / local state | Xcode cache có thể |
| CONFIG | 3 | app config | Không |
| CANON_MEMORY | 1.1 | governance | Không |
| REBUILDABLE_CACHE | ~3 | cache | Có (thấp) |

**Debt lớn nhất:**
1. Multi-model store redundancy (71 GB).
2. Multi-IDE redundancy (25+ GB dormant).
3. OpenAPI port sprawl (coordination cost).

---

## IX. GROSS COORDINATION VALUE

| Nhiệm vụ | Gross Value | Lý do |
|---|---|---|
| Docker recovery | VERY_POSITIVE | Giữ toàn bộ data, tạo margin, ghi policy vào Canon |
| HyperAI governance/memory | VERY_POSITIVE | Shared memory, recovery policy, canon |
| Local model serving | POSITIVE_WITH_DEBT | Ollama là shared runtime; LM Studio/AITK tạo debt |
| OpenAPI primitives | POTENTIAL_HIGH_WITH_FRICTION | 18 capability nhưng thiếu registry |
| Multi-IDE redundancy | NEGATIVE_IF_UNIFIED | 25G dormant, overlapping capability |
| Multi-model stores | POSITIVE_BUT_STORAGE_DEBT_HIGH | fallback value cao nhưng duplicate nhiều |

**Tổng kết:**
- `SUM(verified local value)` cao.
- `coordination_gain` cao ở Docker recovery, OpenAPI, shared model runtime.
- `duplicated_compute` lớn ở IDE và model store.
- `coordination_friction` lớn ở OpenAPI port sprawl.
- `unresolved_debt` nằm ở ECONOMICS axis (không ai chịu trách nhiệm storage budget).

---

## X. TRỤC THIẾU NGƯỜI CHỊU TRÁCH NHIỆM

### ECONOMICS — AXIS_UNDERSTAFFED

**Vấn đề:** Không có actor nào nắm budget compute/storage. Ollama, LM Studio, AITK, Pieces đều chỉ claim capability nhưng không gánh trách nhiệm tổng.

**Hậu quả:**
- Disk lên 96%.
- Docker recovery phải can thiệp khẩn cấp.
- Model download tiếp theo có thể gây lại pressure.
- Không có admission policy cho workload nặng.

**Ứng cử viên nắm trục:**
- HyperAI OS Master: có survival governor role.
- Docker Desktop: có resource accounting nhưng chỉ cho container.
- Devin: là operator, không phải policy setter.

**Kiến nghị:** HyperAI OS Master hoặc Agent OS nên nắm ECONOMICS với input từ `docker_workload_admission_policy.json` và `docker_storage_ledger.json`.

### FORMAL_LOGIC — AXIS_UNDERSTAFFED

**Vấn đề:** DAIOF-Framework có codebase nhưng không có active runtime. OpenAPI fabric có `bitcoin-price-predictor` và `sql` nhưng chưa có reasoning engine.

**Kiến nghị:** Wake hoặc bind DAIOF-Framework vào một OpenAPI server hoặc runtime.

---

## XI. ACTOR CÓ CAPABILITY NHƯNG CHƯA NHẬN TRÁCH NHIỆM

| Actor | Capability | Authority chưa gánh | Rủi ro |
|---|---|---|---|
| OpenAPI Home Fabric | 18 tool servers | GOVERNANCE | Port sprawl, route drift |
| LM Studio | local model runtime | EXECUTION (primary) | Storage overclaim, không được dùng nhiều |
| AITK | ONNX model runtime | ECONOMICS | Dormant, variants, incomplete download |
| VS Code family | editor | EXECUTION | Dormant 17G+, không active |
| Agent OS | mission dispatch | GOVERNANCE | Authority claim chưa xác minh |
| APO Gateway | service routing | GOVERNANCE | Route contract chưa rõ |

---

## XII. ARTIFACTS SINH RA

Các artifact truy được về evidence thật:

1. `ANDY_SUPERSYSTEM_MAP.json` — toàn bộ actor, trục, capability, runtime, debt.
2. `APO_AXIS_CAPABILITY_RESPONSIBILITY_MATRIX.json` — 8 trục, holder, gap, overclaim.
3. `STORAGE_CAPABILITY_LINEAGE_LEDGER.json` — classification storage theo capability lineage.
4. `MODEL_RUNTIME_LINEAGE_GRAPH.json` — model fabric, cross-store duplicates, lineage.
5. `OPENAPI_HOME_CAPABILITY_MAP.json` — 18 server, port, capability, trạng thái.
6. `PORT_AUTHORITY_AND_ROUTE_MAP.json` — port authority, health, process, conflict.
7. `RUNTIME_COORDINATION_VALUE_GRAPH.json` — nodes, edges, value flows.
8. `GROSS_COORDINATION_VALUE_LEDGER.json` — gross value per mission.
9. `APO_SERVICE_HEALTH_MATRIX.json` — 14/14 APO tools healthy qua proxy; credential broker healthy.
10. `APO_CAPABILITY_NETWORK_DISCOVERY.json` — transport planes, network graph, lineage per server.
11. `APO_CAPABILITY_NETWORK_DISCOVERY.md` — readable summary.
12. `APO_CAPABILITY_MISSION_TRACE.json` — một mission thực: AIOS → APO → time OpenAPI → memory.
13. `APO_CAPABILITY_MISSION_TRACE_WEATHER.json` — weather + memory mission.
14. `APO_CAPABILITY_MISSION_TRACE_SUMMARIZER.json` — summarizer + Ollama mission.
15. `APO_CAPABILITY_MISSION_TRACE_FILESYSTEM.json` — filesystem write/read mission.
16. `APO_CAPABILITY_MISSION_TRACE_EXTERNAL_RAG.json` — RAG retrieval mission (đã sửa langchain API drift).
17. `APO_CAPABILITY_MISSION_TRACE_SQL.json` — DATA axis schema + nl-to-sql mission.
15. `ANDY_HOME_ACTIVE_DEPENDENCY_MAP_raw.json` — process → top-level dir mapping.
16. `ANDY_HOME_CATALOG_PARSED.json` — parsed canonical HOME_CATALOG.
17. `ANDY_HOME_DEPENDENCY_SURFACES.md` — dependency/authority classification per home surface.
18. `MODEL_FABRIC_RECLAMATION_PLAN.json` — plan xóa duplicate an toàn với explicit gate.
19. `RECLAIM_DORMANT_OPERATOR_AND_CACHE_20260731.json` — reclaim 1.25 GB dormant operator runtime + data_backup_cache.

Tất cả nằm trong:
<ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/" />

---

## XIII. NEXT SINGLE STEP — KHÔNG HỎI CREATOR CHỌN A/B/C

Dựa trên `InformationGain + DependencyUnlock + AxisClarity + FutureValue - Risk - ComputeCost - HumanBurden`, bước tiếp theo có giá trị cao nhất là:

**1. Bổ sung health/lease matrix cho APO tools registry (non-destructive) — ĐÃ THỰC HIỆN.**

Kết quả:
- `APO_SERVICE_HEALTH_MATRIX.json` đã tạo. 14/14 tool healthy qua proxy APO Gateway.
- Credential broker `:8765` healthy, 9 active keys, 4 expired leases.
- APO Gateway proxy /tools/{name}/... hoạt động.
- 4 dormant server (auth x3, mcp-proxy) chưa có trong registry.

**2. Sau đó: Audit model fabric duplicate để giảm storage debt.**

Kết quả:
- `MODEL_FABRIC_RECLAMATION_PLAN.json` đã tạo.
- Candidate: nomic-embed duplicate ~800 MB, 3 AITK CUDA variants ~2.4 GB, incomplete 14B download, staged Bionic update ~500 MB.
- Tổng ước tính: 3.7-18 GB tùy incomplete download.

Gate:
- Tôi sẽ không xóa gì cho đến khi nhận được xác nhận duy nhất (một từ: "go" hoặc "approve") cho từng candidate.

---

## XIV. VERDICT LIST

- `ANDY_SUPERSYSTEM_BOUND`: YES
- `STORAGE_CAPABILITY_LINEAGE_BOUND`: YES
- `MODEL_FABRIC_BOUND`: YES
- `OPENAPI_HOME_FABRIC_BOUND`: YES
- `PORT_AUTHORITY_BOUND`: YES
- `AXIS_CANDIDATES_IDENTIFIED`: YES
- `AXIS_HOLDER_VERIFIED`: PARTIAL (EXECUTION, DATA, LANGUAGE, VISION, GOVERNANCE ok; ECONOMICS, LOGIC, FORMAL_LOGIC understaffed)
- `AXIS_RESPONSIBILITY_GAP_FOUND`: YES (ECONOMICS, FORMAL_LOGIC)
- `COORDINATION_VALUE_VERIFIED`: YES
- `GROSS_SYNERGY_VERIFIED`: PARTIAL
- `APO_SUPERSYSTEM_UNDERSTOOD`: PARTIAL
- `SYSTEM_DISCOVERY_PARTIAL`: YES

---

## XV. FINAL LAW APPLIED

> Mạnh lên → gánh nhiều hơn.  
> Cầm trục → bảo vệ trục.  
> Nhận authority → nhận hậu quả.  
> Tạo debt → có trách nhiệm sửa debt.  
> Không ai được trao trục vì danh tiếng.  
> Không ai bị cấm lớn lên.  
> Không ai được mạnh lên bằng cách đẩy chi phí cho cả Home.

Hệ đang sống. Không siêu AI. Một nhóm anh em phối hợp.
