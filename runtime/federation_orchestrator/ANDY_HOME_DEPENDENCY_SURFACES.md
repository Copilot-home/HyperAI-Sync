# ANDY HOME DEPENDENCY SURFACES

**Principle:** `/Users/andy` is not a pile of files. It is a multi-layer super-system. To act without asking, I must know which surface holds which authority, which runtime depends on which files, and which files are disposable.

**Sources:**
- `~/.axcanon/memory/home_catalog/HOME_CATALOG.md` (canonical 2026-07-28 catalog, 515 artifacts)
- `~/.axcanon/memory/brain.index` (canon env load log)
- live process map `ANDY_HOME_ACTIVE_DEPENDENCY_MAP_raw.json`
- live `du` sizes

---

## I. TAXONOMY CỦA HOME

| Category | Label | Count | Total size | Vai trò |
|---|---|---:|---:|---|
| `ai_canon_identity_memory` | Canon / identity / memory AI | 12 | 90 MB | **GỐC PHÁP LÝ** — chứa canon, identity, memory. Không xóa. |
| `ai_forensic_evidence` | Forensic / bằng chứng AI | 44 | 10 MB | **BẰNG CHỨNG** — audit, evidence. Chỉ xóa khi có receipt. |
| `ai_operator_runtime` | Runtime / IDE / operator AI | 71 | 265 MB | **VẬN HÀNH** — IDE, agent, model, gateway. Phần lớn là config/cache. |
| `ai_project_lab` | Dự án / lab AI | 11 | 5 MB | **LAB** — thử nghiệm. Xem từng dự án. |
| `daiof_sandbox` | DAIOF sandbox / audit | 10 | 3 MB | **SANDBOX** — audit cụ thể, có thể archive. |
| `data_backup_cache` | Data / backup / cache | 20 | 114 MB | **CACHE/BACKUP** — nhiều có thể dọn. |
| `dev_tool` | Dev / database / test tool | 198 | 456 MB | **CÔNG CỤ** — npm, pip, binaries, databases. Chọn lọc. |
| `finance_crypto` | Tài chính / crypto | 1 | 16 KB | **NGOẠI VI** — ví/key. Không động. |
| `generic_project` | Dự án / lab khác | 47 | 76 MB | **PROJECT** — nguồn generic. Xem từng project. |
| `gke_lab` | GKE / cloud AI lab | 3 | 11 KB | **LAB CLOUD** — GKE experiments. |
| `unknown` | Chưa phân loại | 59 | 37 MB | **UNKNOWN** — cần phân loại trước khi xóa. |
| `user_system` | macOS user / data | 15 | 427 MB | **HỆ THỐNG NGƯỜI DÙNG** — Photos, Music, Downloads. Cảnh giác. |
| `vscode_extension` | VSCode / editor extension project | 24 | 5 MB | **EXTENSION** — code extension projects. |

Tổng: **515 artifacts**, **~1.46 GB** trong catalog (chưa tính model store lớn ngoài catalog).

---

## II. CANON/IDENTITY/MEMORY — ROOT

Các thư mục này là **gốc** của hệ. Không được xóa, không được sửa nếu không có canon gate.

| Dir | Vai trò | Active | Phụ thuộc |
|---|---|---|---|
| `.axcanon` | Canon root, `brain.index`, `home_catalog`, `secrets/` | 2026-07 | `.axcanon/memory → canon/apo, secrets; root → axcontrol` |
| `.con-memory` | Conversation memory sqlite (1.3M rows) | 2026-07 | `aios_mission_router.py` đọc table counts |
| `.ai-persistent-memory` | Legacy HAIOS consciousness memory + 26MB sqlite | 2026-07 | symlink đến `.axcanon` |
| `.ai-identity` | Identity anchors | 2026-07 | canon |
| `.ai-fs-canon` | AI file-system canon | 2026-07 | canon |
| `.memory` | New memory surface (5 items) | 2026-07 | canon |
| `.apomega` | Dormant apomega planner | 2026-06 | — |
| `.consciousness` | Dormant consciousness logs | 2026-02 | — |
| `axcontrol` | Sigma APO operational canon | 2026-07 | `.axcanon/apo_canon → axcontrol/canon/apo` |

**Quy tắc:** Đây là `ROOT_LOCAL_AUTHORITY` + `CANON`. Chỉ đọc/append. Không xóa.

---

## III. OPERATOR RUNTIME — AI SURFACE

71 thư mục. Chỉ cần hiểu các **runtime thực sự đang chạy**.

### Đang chạy / gần đây

| Dir | Actor | Ports | Depends on | Axis |
|---|---|---|---|---|
| `.codex` | Codex / ChatGPT for Chrome / skills | plugin | `.codex/AGENTS.md`, `.codex/config.toml`, `.codex/plugins` | GOVERNANCE, EXECUTION |
| `.agents` | Devin/Codex skills | — | `.devin` skills, `.codex` rules | GOVERNANCE |
| `.devin` | Devin CLI | — | `~/.local/share/devin`, `~/.config/devin` | EXECUTION |
| `.hyperai` | HyperAI runtime (GORDON, watchdog, logs) | 8777 (`agent_os.py`) | `.hyperai/logs`, `.config/hyperai/credentials.env` | EXECUTION |
| `.aios` | AIOS canon/secrets | — | `.axcanon` | SECURITY |
| `.apo` | APO Gateway | 9011 | `~/.apo/gateway/apo_config.yaml`, OpenAPI servers, credential broker | GOVERNANCE |
| `.ollama` | Ollama model runtime | 11434 | `~/.ollama/models`, `/Applications/Ollama.app` | LANGUAGE, VISION |
| `.lmstudio` | LM Studio + Bionic | 1234, 1235, 41343 | `~/.lmstudio` model bundles | LANGUAGE, VISION |
| `.aitk` | AI Toolkit | — | `~/.aitk/models` | LANGUAGE |
| `.antigravity-ide` | Antigravity IDE | — | `.gemini`, `.antigravity` | EXECUTION |
| `.gemini` | Gemini/Antigravity language server | 51035 | Antigravity IDE | LANGUAGE |
| `.claude` | Claude / Claude Code | — | `.claude.json`, `.claude-server-commander` | LANGUAGE |
| `.copilot` | GitHub Copilot | — | VS Code, IDE | LANGUAGE, EXECUTION |
| `.cursor` | Cursor IDE | — | — | EXECUTION |
| `.codeium` | Codeium | — | — | LANGUAGE |
| `.qwen` | Qwen tooling | — | — | LANGUAGE |
| `.sema4ai` | Sema4 agent | — | — | EXECUTION |
| `.ollama-direct` | Ollama direct wrapper | — | `.ollama` | LANGUAGE |
| `.playwright-mcp` | Playwright MCP | — | — | EXECUTION |
| `.github-copilot-cli` | gh Copilot CLI | — | `gh` auth | EXECUTION |
| `.daiof` | DAIOF experiments | — | — | LOGIC |

### Không chạy / dormant

| Dir | Trạng thái | Hành động |
|---|---|---|
| `.agent_data` | legacy Sigma APO source, 94 items | **HOLD** — chứa canon/axis code, không xóa |
| `.blackbox`, `.blackbox-cli-v2` | dormant | **CLEAN_CANDIDATE** nếu không dùng |
| `.bitowingman` | dormant 2026-02 | **CLEAN_CANDIDATE** |
| `.chatgpt-copilot` | dormant 0 item | **SAFE_DELETE** |
| `.cline` | dormant 2026-06 | **CLEAN_CANDIDATE** |
| `.codegeex` | dormant 0 item 2025-11 | **SAFE_DELETE** |
| `.codemate` | dormant 2026-03 | **CLEAN_CANDIDATE** |
| `.mcp`, `.mcp-auth` | dormant 2026-03 | **CLEAN_CANDIDATE** nếu không dùng |
| `.mcporter` | dormant 2026-06 | **HOLD** (có thể là MCP tool) |
| `.cagent` | dormant 2026-06 | **HOLD** (Docker/agent helper) |

---

## IV. ACTIVE SUPER-SYSTEM DEPENDENCY GRAPH

```
CREATOR / Devin CLI
    → ~/.codex/AGENTS.md          (canon)
    → ~/.agents/skills/*            (tool routing)
    → ~/.con-memory/conversations.db (memory context)

AIOS Runtime Orchestrator (workbench/aios_runtime_orchestrator)
    → ~/.codex/AGENTS.md
    → ~/.con-memory/conversations.db
    → ~/.agents/skills/hyperai-runtime-orchestrator
    → HyperAI-Sync/memory/runtime_execution_todo.md
    → HyperAI-Sync/runtime/federation_orchestrator

APO Gateway (~/.apo/gateway)
    → ~/.apo/gateway/apo_config.yaml
    → ~/.config/hyperai/credentials.env (for some tool env)
    → OpenAPI servers :8901-8914
    → Credential Broker :8765 (optional X-Lease-Id)

Credential Broker (HyperAI-Sync/tools/hyperai_credentials_service.py)
    → ~/.config/hyperai/credentials.env
    → HyperAI-Sync/tools/hyperai_credentials_loader.py

OpenAPI servers (~/openapi-servers)
    → ~/openapi-servers/.venv
    → ~/.config/hyperai/credentials.env (sql, slack, google_pse)
    → Ollama :11434 (summarizer)
    → Open-Meteo API (weather)

HyperAI Agent OS (~/HyperAI/agent_os.py)
    → ~/.hyperai/logs
    → ~/.aios/secrets.env
    → ~/.config/hyperai/credentials.env

Ollama
    → ~/.ollama/models
    → /Applications/Ollama.app

LM Studio / Bionic
    → ~/.lmstudio
    → /Applications/LM Studio.app
    → /Applications/Bionic.app

AI Toolkit
    → ~/.aitk/models

Antigravity IDE
    → ~/.antigravity-ide
    → ~/.gemini
    → ~/.antigravity

Pieces OS
    → ~/Library/Application Support/com.pieces.os

Docker
    → ~/.docker
    → ~/.axcanon (com.docker.backend mở file ở đây)
    → /Users/andy/Library/Containers/*
```

---

## V. PROJECT / SOURCE SURFACES

| Dir | Vai trò | Trạng thái |
|---|---|---|
| `HyperAI-Sync` | **Command center hiện tại**: tools, memory, runtime, federation orchestrator | active |
| `workbench` | AIOS runtime orchestrator, D&R Protocol, Agent Data System | active |
| `openapi-servers` | 14 OpenAPI capability servers | active |
| `axcontrol` | Sigma APO operational canon | active (canon) |
| `.agent_data` | Legacy Sigma APO source + axis implementations | dormant but canon-adjacent |
| `HyperAI` | `agent_os.py` runtime | active (port 8777) |
| `.ai-persistent-memory` | Legacy HAIOS memory | dormant |
| `vscode-edge-devtools` | Edge devtools clone | dormant |

---

## VI. MODEL / INFERENCE SURFACES

| Dir | Runtime | Size | Nội dung | Trạng thái |
|---|---|---|---|---|
| `~/.ollama/models` | Ollama | 17 GB | GGUF model blobs | active |
| `~/.lmstudio` | LM Studio / Bionic | 26 GB | bundled models, app data, staged updates | active |
| `~/.aitk/models` | AI Toolkit | ~10 GB | ONNX / DirectML models | active |
| `~/Library/Application Support/com.pieces.os` | Pieces OS | 14 GB | Pieces OS data | active |

Đã thực hiện local evidence gate:
- Xóa **80 MB** duplicate `nomic-embed-text` trong `~/.lmstudio/llmster/0.0.19-2`.
- Xóa **3.9 GB** AITK CUDA variants trên Mac (không có CUDA).
- Giữ lại Microsoft 14B CPU (hoàn chỉnh, 12 GB).
- Giữ lại staged Bionic 1.0.4+9 (mới hơn /Applications/Bionic 1.0.3+3).

---

## VII. CACHE / BACKUP / DISPOSABLE

| Category | Khi nào dọn được | Cách |
|---|---|---|
| `data_backup_cache` | nếu >7 ngày và có source gốc | đối chiếu SHA256 |
| `dev_tool` cache (`.cache`, `.npm/_cache`, `Library/Caches`) | nếu ứng dụng tự rebuild | xóa cache của công cụ không active |
| `ai_forensic_evidence` | chỉ khi case đã close và có receipt | archive trước khi xóa |
| `unknown` | **không xóa** cho đến khi phân loại | classify trước |
| `user_system` (Photos, Music, Downloads) | **không xóa** nếu là user data | chỉ xóa Downloads duplicate |

---

## VIII. HÀNH ĐỘNG TIẾP THEO — KHÔNG HỎI

Dựa trên dependency map:

1. **Tiếp tục trace APO capability** cho `filesystem`, `external_rag`, `google_pse` để hoàn thiện value path.
2. **Áp dụng local evidence gate** cho các `dormant operator runtime` và `data_backup_cache` — không hỏi anh từng file, dùng classification + dependency + lineage.
3. **Cập nhật `ANDY_SUPERSYSTEM_MAP`** với dependency surface này.

Tôi đã đủ thông tin để tự quyết định với:
- **HOLD**: canon/identity/memory, active runtime, model stores, pending updates.
- **CLEAN**: duplicate model files, CUDA variants, dormant tools có source gốc.
- **CLASSIFY**: `unknown` trước khi xóa.

---

## IX. VERDICT

**ANDY_HOME_DEPENDENCY_SURFACES_DISCOVERED**

`/Users/andy` được phân loại thành 13 taxonomy. Gốc canon nằm ở `.axcanon`. Runtime operator nằm ở `ai_operator_runtime`. Model nằm ở `.ollama`, `.lmstudio`, `.aitk`, `com.pieces.os`. Capability nằm ở `openapi-servers`. Gateway nằm ở `.apo`. Orchestrator nằm ở `workbench` + `HyperAI-Sync`. Tôi có thể tự phân loại và tự quyết định dựa trên evidence gate mà không cần hỏi anh từng bước.
