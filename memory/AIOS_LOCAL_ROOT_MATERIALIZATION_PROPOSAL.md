# AIOS Local Root Control Plane — Materialization Proposal

Date: 2026-07-30
Status: proposal, awaiting creator gate

## 1. Diagnosis (creator insight)

Hệ thống HyperAI/AIOS đã có topology đầy đủ, nhưng chưa có một **Root Local** thực sự nắm đủ quyền lực:

```text
whole-local view + shell authority + asset authority + runtime control
+ verification + recovery + single mission root
```

Từng surface hiện tại đều bị giới hạn:

| Surface | Có | Chưa có |
|---|---|---|
| federation_orchestrator | route, registry, drift guard | shell authority |
| codex_operator_runtime | worker, reasoning | authority |
| memory_writer | write canon | runtime control |
| verification_truth | verify | execution |
| apo_gateway | provider routing | local asset registry |
| product_runtime | product shell authority | cross-platform |

Kết quả:

```text
∀ s_i, Authority(s_i) ⊊ D_local
```

`SingleMissionRoot = 1` đã được viết trong canon, nhưng **chưa được materialize thành runtime thực**.

## 2. Local Root đã tồn tại

`/Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py` đã hiện hữu và verify PASS:

- `verify.run` trả về 16/16 check PASS.
- Có stack: `CRP -> MRP -> RBE -> OODA -> EEC -> PMP -> DAK`.
- Có `runtime_registry.json`, `mrp_registry.json`.
- Có non-negotiable invariants: no fabrication, no guessing, no auto-discovery, no auto-binding, no auto-execution, no auto-scheduling, no auto-mutation.

**Vấn đề:** router đang ở trạng thái khai sinh — chưa được nâng thành runtime daemon, chưa có registry đầy đủ của toàn bộ local surfaces, và chưa thay thế `python tools/hyperai_autonomous_cycle.py` làm entrypoint mặc định.

## 3. Đề xuất kiến trúc Local Root

```text
Creator
  ↓
Local Root Control Plane (aios_mission_router daemon)
  ├── federation_orchestrator      (mission routing + registry)
  ├── memory_writer                (single evidence recorder)
  ├── verification_truth           (runtime probe + proof gate)
  ├── codex_operator_runtime       (worker surface)
  ├── apo_gateway 9011             (provider + tool proxy)
  ├── credential broker 8765       (secret lease)
  ├── ollama 11434                 (local inference)
  ├── lmstudio/bionic 1235         (local inference)
  ├── openapi tool servers 8901+   (tools)
  ├── docker mcp gateway 8811      (MCP tools)
  ├── product runtime Mac          (portable projection)
  └── product runtime Windows      (canonical, optional)
```

Local Root là **mission router + gatekeeper**, không phải thay thế Creator. Creator vẫn là approval lane.

## 4. Thứ tự 9 bước đã chốt

| # | Bước | Surface | Hành động chính | Gate |
|---|---|---|---|---|
| 1 | Materialize Local Root | `workbench/aios_runtime_orchestrator` | Chạy router như daemon/launchd, cập nhật AGENTS.md entrypoint | explicit (macos control) |
| 2 | Khôi phục shell authority | `shell_authority` | Disk stable, no reset, xác thực qua health probe | verification gate |
| 3 | Sửa Docker không reset | `docker_fabric` | Inspect -> repair daemon, socket, volume; không factory reset | PMP (no reset) |
| 4 | Tách product runtime khỏi federation | `federation_orchestrator` | Coi product runtime là optional degraded; federation hoạt động độc lập | canon update |
| 5 | Dựng Mac projection | `hyperai_product_runtime` | Tạo `hyperai-user-control-system-mac` hoặc portable build | implementation |
| 6 | Sửa credentials và Bionic worker | `apo_gateway`, `lmstudio` | Thêm Slack/PSE keys, sửa Bionic embedding worker hoặc route-around Ollama embedding | creator provides keys |
| 7 | Làm sạch Git + rollback | `git_sync_transport` | Commit/stash dirty repos, tạo rollback bundles | git authority |
| 8 | Mở Telegram | `telegram_relay` | Auth verified, command scope bound, audit trail | shell authority healthy |
| 9 | Mở first-dollar economy | `telegram_treasury_economy` | Budget cap, ledger writer, kill switch, rollback test | last gate |

## 5. Nhiệm vụ cấp bách nhất: Materialize Local Root

### 5.1 Runtime registry đầy đủ

Cập nhật `/Users/andy/workbench/aios_runtime_orchestrator/runtime_registry.json` để liệt kê tất cả local surfaces:

```json
{
  "version": 2,
  "nodes": [
    {"id": "apo_gateway", "kind": "http_service", "port": 9011, "health_path": "/health"},
    {"id": "credential_broker", "kind": "http_service", "port": 8765, "health_path": "/status"},
    {"id": "ollama", "kind": "http_service", "port": 11434, "health_path": "/api/tags"},
    {"id": "lmstudio_bionic", "kind": "http_service", "port": 1235, "health_path": "/v1/models"},
    {"id": "openapi_time", "kind": "http_service", "port": 8901, "health_path": "/health"},
    ...
  ]
}
```

### 5.2 Command surfaces

Các lệnh Local Root sẽ trở thành entrypoint mặc định:

```bash
# Verify whole local ecosystem
python /Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py verify.run

# Plan a mission
python /Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py mission.plan \
  --mission-text "Verify all local tool surfaces return 200" \
  --target-surface verification_truth \
  --risk-class runtime_check \
  --requested-action read

# Route to skill
python /Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py skills.route \
  --mission-text "Docker inspection without reset"
```

### 5.3 macOS LaunchAgent (daemon)

Tạo `~/Library/LaunchAgents/aios.mission.router.plist` để Local Root luôn chạy, lắng nghe port `9001` hoặc UNIX socket, và expose:

- `GET /health`
- `POST /mission/plan`
- `POST /runtime/verify`
- `POST /surface/control`

Không bind `0.0.0.0` trừ khi explicit gate.

### 5.4 Single Creator Cockpit

Local Root expose một dashboard JSON/API cho Creator:

```json
{
  "runtime_status": { "healthy": [...], "degraded": [...], "missing": [...] },
  "active_missions": [...],
  "pending_approval": [...],
  "economy_state": "blocked",
  "shell_authority": "degraded",
  "disk_state": "STABLE"
}
```

Creator vẫn là approval lane; Local Root chỉ điều phối và gate.

## 6. Phản hồi ba câu hỏi

### 6.1 Product runtime Windows-only

Không bắt federation phụ thuộc product runtime. Cách xử lý:

- Product runtime Windows là canonical lane.
- Dựng `hyperai-user-control-system-mac` (projection) chạy local-first.
- Trong thời gian chuyển đổi, federation vẫn hoạt động với tool surfaces + APΩ.
- Port 5000/4173 stale được coi là `optional_degraded`, không kéo cycle.

### 6.2 Docker degraded

```text
Preserve -> Inspect -> Repair (no reset)
```

Route-around fakeAPI/remote chỉ là tạm thời, không thay thế local mastery.

Thứ tự:
1. Inventory container/image/volume/network.
2. Chụp state + evidence.
3. Xác định lỗi daemon/socket/volume/compose.
4. Sửa đúng tầng.
5. Smoke test.
6. Restore OpenAPI/MCP gateway.

### 6.3 Unblock Economy/Telegram

`UnblockEconomy = 1` chỉ khi:

```text
ShellAuthority = healthy
∧ GitState = recoverable
∧ CredentialBroker = healthy
∧ VerificationGate = PASS
∧ SingleLedgerWriter = 1
∧ BudgetCap > 0
∧ KillSwitch = 1
∧ RollbackTested = 1
```

Telegram mở khi: `AuthVerified + CommandScopeBound + AuditTrail + NoDirectShell`.

## 7. Next action

Mở gate cho bước 1: **Materialize Local Root**.

Cụ thể:
1. Chạy `aios_mission_router.py` như daemon.
2. Cập nhật `AGENTS.md` entrypoint từ `hyperai_autonomous_cycle.py` sang `aios_mission_router.py`.
3. Cập nhật `runtime_registry.json` với toàn bộ local surfaces.
4. Viết `verify.run` cho toàn bộ hệ sinh thái.

Creator cần approve bước này trước khi thực hiện.
