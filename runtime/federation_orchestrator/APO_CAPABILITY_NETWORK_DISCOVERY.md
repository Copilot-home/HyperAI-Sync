# APO CAPABILITY NETWORK DISCOVERY

**Execution ID:** apo-capability-network-discovery-20260731  
**Timestamp:** 2026-07-31T14:10:00Z  
**Principle:** Capability is not the server. Capability is the value path across source, build, runtime, route, auth, and memory.

---

## I. PHÁN QUYẾT

Mạng trong `/Users/andy` không chỉ là Docker. Docker là một trong nhiều **transport plane**.

APO network hiện gồm:

```text
HOST_LOOPBACK
DOCKER_BRIDGE
HOST_PORT_FORWARDING
UNIX_SOCKET
HTTP_OPENAPI
REDIS
MCP_STDIO
PLUGIN_RUNTIME
LEASE_GATED_PROXY
MISSION_ROUTING
```

14 OpenAPI server đang chạy trên `127.0.0.1:8901-8914` như các process uvicorn trên host. Không server nào đang chạy trong Docker. Docker vẫn đang nuôi kind cluster và registry.

APO Gateway (`:9011`) đã làm đường phố: nó nhận `/tools/{name}/{path}` và proxy đến đúng server. Credential Broker (`:8765`) làm cửa gate khi cần lease.

AIOS Runtime Orchestrator (`:9001`) làm điều phối mission: nó chọn skill và cho phép hành động nào.

Tôi đã chạy một mission thực:

```
Devin (mission: get UTC time)
→ AIOS :9001 /mission/plan
→ APO Gateway :9011 /tools/time/get_current_utc_time
→ time server :8901
→ JSON UTC time
→ Devin verify
→ update_memory.py ghi HyperAI-Sync memory
```

Artifact chứng minh:
<ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/APO_CAPABILITY_MISSION_TRACE.json" />

---

## II. TRANSPORT PLANES

| Plane | Vai trò | Ví dụ | Verified |
|---|---|---|---|
| HOST_LOOPBACK | Giao tiếp process trên cùng host | APO :9011, OpenAPI :8901-8914, AIOS :9001 | YES |
| DOCKER_BRIDGE | Mạng container Linux | kind cluster, registry | YES |
| HOST_PORT_FORWARDING | publish container port ra host | 62056→kind | YES |
| UNIX_SOCKET | IPC nội bộ | docker.sock | unknown |
| HTTP_OPENAPI | Route OpenAPI qua HTTP | `/tools/time/get_current_utc_time` | YES |
| REDIS | Shared state | `:6379` | listening |
| MCP_STDIO | MCP over stdio | IDE plugin | unknown |
| PLUGIN_RUNTIME | Runtime của các app | LM Studio, Pieces, Antigravity | YES |
| LEASE_GATED_PROXY | Auth qua lease | Credential Broker + APO X-Lease-Id | YES (broker healthy, not stress-tested) |
| MISSION_ROUTING | Điều phối mission | AIOS `/mission/plan`, `/skills.route` | YES |

---

## III. CAUSAL CHAIN CỦA MỘT MISSION

Mission: **Lấy thời gian UTC và lưu vào bộ nhớ.**

| Stage | Actor | Surface | Output | Trạng thái |
|---|---|---|---|---|
| MISSION | Devin | user chat | "get UTC time" | received |
| PLAN | AIOS Runtime Orchestrator | `:9001/mission/plan` | skill plan, allowed surfaces | PLANNED |
| ROUTE | APO Gateway | `:9011/tools/time/get_current_utc_time` | time JSON | ROUTABLE |
| AUTH | Credential Broker | `:8765` | not invoked (public tool) | not needed |
| EXECUTE | time OpenAPI server | `:8901` | UTC timestamp | EXECUTED |
| VERIFY | Devin | JSON parser | format ok | VERIFIED |
| MEMORY | update_memory.py | `HyperAI-Sync/memory/work_journal.md` | memory updated | PERSISTED |

Giá trị gộp: một mission đi xuyên qua 4 actor (AIOS, APO, OpenAPI, memory) và tạo ra value lớn hơn time server đứng riêng.

---

## IV. TRẠNG THÁI CỦA MỖI OPENAPI SERVER

Từng server được phân loại theo các trạng thái:

```text
SOURCE_PRESENT  →  BUILT  →  REGISTERED  →  ROUTABLE  →  LISTENING  →  RESPONSIVE  →  MISSION_USED  →  VALUE_VERIFIED  →  HISTORICAL
```

| Server | Port | Transport | Dockerfile | Runtime | APO Route | Responsive | Mission-Used |
|---|---|---|---|---|---|---|---|
| time | 8901 | HTTP_OPENAPI | yes | host uvicorn | `/tools/time/*` | YES | YES |
| weather | 8902 | HTTP_OPENAPI | yes | host uvicorn | `/tools/weather/*` | YES | NO |
| filesystem | 8903 | HTTP_OPENAPI | yes | host uvicorn | `/tools/filesystem/*` | YES | YES (Devin used) |
| git | 8904 | HTTP_OPENAPI | yes | host uvicorn | `/tools/git/*` | YES | NO |
| memory | 8905 | HTTP_OPENAPI | yes | host uvicorn | `/tools/memory/*` | YES | NO |
| quotes | 8906 | HTTP_OPENAPI | yes | host uvicorn | `/tools/quotes/*` | YES | NO |
| flashcards | 8907 | HTTP_OPENAPI | yes | host uvicorn | `/tools/flashcards/*` | YES | NO |
| time_ui | 8908 | HTTP_OPENAPI | yes | host uvicorn | `/tools/time_ui/*` | YES | NO |
| summarizer | 8909 | HTTP_OPENAPI | yes (compose) | host uvicorn | `/tools/summarizer/*` | YES | NO |
| bitcoin | 8910 | HTTP_OPENAPI | no | host uvicorn | `/tools/bitcoin/*` | YES | NO |
| sql | 8911 | HTTP_OPENAPI | no | host uvicorn | `/tools/sql/*` | YES | NO |
| external_rag | 8912 | HTTP_OPENAPI | no | host uvicorn | `/tools/external_rag/*` | YES | NO |
| slack | 8913 | HTTP_OPENAPI | yes | host uvicorn | `/tools/slack/*` | YES | NO |
| google_pse | 8914 | HTTP_OPENAPI | yes | host uvicorn | `/tools/google_pse/*` | YES | NO |

Dormant (chưa trong APO registry, chạy port 8000 nếu khởi động):

- `get-oauth-tokens`, `get-tokens-from-cookies`, `get-user-info` (auth variants)
- `mcp-proxy`

---

## V. DOCKER KHÔNG PHẢI TOÀN BỘ MẠNG

Docker đang chạy:

```text
kind-cloud-provider
kind-registry-mirror
desktop-control-plane
prizz_deep-dive-desktop-extension-service
```

Không có OpenAPI server nào trong container. Tất cả OpenAPI server đều chạy bằng `uvicorn` từ `/Users/andy/openapi-servers/.venv` trên host.

Docker vẫn là một **substrate quan trọng**:

- build capability
- package capability
- network isolation
- ephemeral instances
- kind cluster

Nhưng Docker không sở hữu OpenAPI capability network. Capability identity đến từ:

```text
source + role + route + lineage + mission value
```

---

## VI. AUTHORITY VÀ ROUTE

| Actor | Authority |
|---|---|
| AIOS Runtime Orchestrator | chọn mission → skill → allowed surface |
| APO Gateway | tra registry `tools` và proxy request |
| Credential Broker | cấp X-Lease-Id nếu tool yêu cầu auth |
| OpenAPI Server | thực thi capability |
| Devin / Agent | tiêu thụ output và verify |
| HyperAI-Sync memory | lưu trace và receipt |

Quy tắc:

```text
Capability mạnh lên → trách nhiệm tăng.
Cầm route → chịu trách nhiệm route.
Cầm server → chịu trách nhiệm availability và recovery.
Cầm trục → gánh trục.
```

---

## VII. MISSION TRACE STATUS

| Capability | Verdict | Mission artifact |
|---|---|---|
| `time` | ✅ VALUE_VERIFIED | `APO_CAPABILITY_MISSION_TRACE.json` |
| `weather` | ✅ VALUE_VERIFIED | `APO_CAPABILITY_MISSION_TRACE_WEATHER.json` |
| `memory` | ✅ VALUE_VERIFIED | `APO_CAPABILITY_MISSION_TRACE_WEATHER.json` |
| `summarizer` | ✅ VALUE_VERIFIED | `APO_CAPABILITY_MISSION_TRACE_SUMMARIZER.json` |
| `filesystem` | ✅ VALUE_VERIFIED | `APO_CAPABILITY_MISSION_TRACE_FILESYSTEM.json` |
| `external_rag` | ✅ VALUE_VERIFIED (after fix) | `APO_CAPABILITY_MISSION_TRACE_EXTERNAL_RAG.json` |
| `sql` | ✅ VALUE_VERIFIED (after fix) | `APO_CAPABILITY_MISSION_TRACE_SQL.json` |
| `google_pse` | ❌ FAILURE_EDGE_VERIFIED | `APO_CAPABILITY_MISSION_TRACE_GOOGLE_PSE.json` |
| `bitcoin` | ⚠️ ENDPOINT_HEALTHY_ROUTE_PROVEN_VALUE_NOT_VERIFIED | `APO_CAPABILITY_MISSION_TRACE_BITCOIN_PREDICTOR.json` |

Còn lại: `slack`, `quotes-ui`, `flashcards`, `time-ui`.

## VIII. NEXT SINGLE STEP

Dựa trên `InformationGain + DependencyUnlock + FutureComputeSaved + StorageValue - Risk - RecoveryDebt`:

1. ✅ Đã sửa `sql` output parsing — `sql/main.py` được patch, restart, value verified.
2. ✅ Đã reclaim `dormant operator runtime` + `data_backup_cache` — 1.25 GB freed.
3. Nếu cần thêm capability edge → trace `slack` hoặc các UI-capability còn lại.

Tổng storage đã giải phóng trong session: **5.23 GB** (3.98 GB model fabric + 1.25 GB dormant runtime/cache).

---

## VIII. VERDICT

**APO_CAPABILITY_NETWORK_DISCOVERED**

Mạng có nhiều transport plane. OpenAPI servers chạy trên host loopback, được APO Gateway route. Một mission `time` đã được trace từ AIOS plan → APO → OpenAPI → memory. 13 server còn lại responsive nhưng chưa mission-verified. Docker là substrate riêng, không phải runtime plane cho OpenAPI fabric.
