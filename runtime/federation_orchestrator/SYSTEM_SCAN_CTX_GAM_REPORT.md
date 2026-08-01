# SYSTEM_SCAN_CTX_GAM REPORT

*Execution: system-scan-ctx-gam-20260731*  
*Scope: /Users/andy + live runtime*  
*Mode: disk + runtime-context + audit*  
*Timestamp: 2026-07-31T13:40:00Z*

## EXECUTIVE SUMMARY

`/System/Volumes/Data` is at **96%** capacity with **19 GiB free** after Docker recovery and fossil reconciliation. The largest disk blocks are AI model stores, IDE user data, app sandboxes, media, and project repos. Multiple local AI runtimes are active (Ollama, LM Studio, Antigravity, Pieces, Phoenix, FinalAI, openapi-servers, agent_os, apo_gateway). One port conflict was found: **port 5000 is bound by `ControlCe` (Control Center)**, not by the expected HyperAI backend.

## 1. DISK BASELINE

```
Filesystem      Size    Used   Avail Capacity
/dev/disk3s1   460Gi   393Gi    19Gi    96%
```

Top-level `/Users/andy` by size (tail -40):

- `Library`                                  89 GiB
- `.lmstudio`                                26 GiB
- `.ollama`                                  17 GiB
- `.aitk`                                    14 GiB
- `.vscode`                                  11 GiB
- `Pictures`                                  9.3 GiB
- `projects`                                  7.2 GiB
- `Archive`                                   5.1 GiB
- `.vscode-insiders`                          6.8 GiB
- `workbench`                                 3.6 GiB
- `.codeium`                                  3.2 GiB
- `.config`                                   3.0 GiB
- `.local`                                    2.8 GiB
- `.codex`                                    2.7 GiB
- `.antigravity-ide`                          1.4 GiB
- `.cache`                                    1.5 GiB
- `.venv`                                     1.7 GiB
- `.rustup`                                   1.3 GiB
- `.codemate`                                 1.1 GiB
- `HyperAI-Sync`                              1.1 GiB
- `Library/com.pieces.os`                    14 GiB
- `Library/Application Support`              37 GiB
- `Library/Containers`                       13 GiB
- `Library/Mail`                              4.6 GiB
- `Library/Group Containers`                  4.9 GiB
- `Library/Developer`                         5.9 GiB

## 2. CU_DISK

```text
- cu_d1: span_hint="Library/Application Support ~37G", meaning="Application data, IDE user profiles, extensions, caches. Contains VSCodium (10G), VS Code (3.4G), VS Code Insiders (3.2G), Antigravity (2.5G), Notion (1.9G), BLACKBOXAI (1.1G). Mix of user state and rebuildable cache.", role=data
- cu_d2: span_hint="Library/com.pieces.os ~14G", meaning="Pieces OS on-device model / index / production data. Active runtime dependency.", role=model
- cu_d3: span_hint="Library/Containers ~13G", meaning="App sandbox containers. Docker Desktop (7.1G), Apple Mail (2.2G), Safari (1G), Slack (409M), Telegram, others. Contains runtime state.", role=runtime
- cu_d4: span_hint=".lmstudio ~26G", meaning="LM Studio model storage and runtime data. Active local model runtime.", role=model
- cu_d5: span_hint=".ollama ~17G", meaning="Ollama model storage. Active local model runtime with qwen3, siri, chatgpt, gpt-5.5, minimax models.", role=model
- cu_d6: span_hint=".aitk ~14G", meaning="AITK / ai-toolkit model and runtime data. Active AI runtime.", role=model
- cu_d7: span_hint=".vscode ~11G", meaning="VS Code extensions, user settings, workspace state. Active editor.", role=runtime
- cu_d8: span_hint=".vscode-insiders ~6.8G", meaning="VS Code Insiders extensions and state. Active editor.", role=runtime
- cu_d9: span_hint="Pictures ~9.3G", meaning="Photos Library.photoslibrary — user media.", role=data
- cu_d10: span_hint="projects ~7.2G", meaning="Source code / project workspace. projects/AI dominates.", role=code
- cu_d11: span_hint="Archive ~5.1G", meaning="HyperAI-Ecosystem archive — historical project data.", role=data
- cu_d12: span_hint="Library/Developer ~5.9G", meaning="Xcode, simulators, developer tool state. Contains caches and device support.", role=runtime
- cu_d13: span_hint=".config ~3.0G", meaning="User config. blackbox/mcp-hermit (2.7G) is dominant. Includes gcloud (105M), opencode (61M), kilo (57M).", role=config
- cu_d14: span_hint=".local ~2.8G", meaning="Local data. devin (926M), uv (299M), claude (210M), gh (107M). Includes installed binaries and state.", role=runtime
- cu_d15: span_hint=".codeium ~3.2G", meaning="Codeium extension / model cache. Active coding assistant.", role=model
- cu_d16: span_hint=".codex ~2.7G", meaning="Codex skills, runtimes, and state. Active AI runtime.", role=runtime
- cu_d17: span_hint=".cache ~1.5G", meaning="User caches. 1.5G is codex-runtimes cache.", role=cache
- cu_d18: span_hint="Library/Caches ~750M", meaning="System / app cache. Rebuildable.", role=cache
- cu_d19: span_hint="Library/pnpm ~819M", meaning="pnpm package store. Rebuildable but used by projects.", role=cache
- cu_d20: span_hint=".Trash ~292M", meaning="Trash contents.", role=cache
- cu_d21: span_hint="Library/Biome ~470M", meaning="Biome / Apple on-device model / indexing data.", role=model
- cu_d22: span_hint="Library/Daemon Containers ~584M", meaning="Apple daemon container data.", role=runtime
- cu_d23: span_hint="docker-recovery ~1.3M", meaning="Failure fossil evidence package retained after raw-image retirement.", role=cache
```

## 3. RELATIONS_DISK

```text
- cu_d4 (.lmstudio) --critical_for--> cu_r_ollama_runtime (local model server)
- cu_d5 (.ollama) --critical_for--> cu_r_ollama_runtime
- cu_d6 (.aitk) --critical_for--> cu_r_aitk_runtime
- cu_d2 (com.pieces.os) --critical_for--> cu_r_pieces_os
- cu_d7 (.vscode) --critical_for--> cu_r_vscode_editor
- cu_d8 (.vscode-insiders) --critical_for--> cu_r_vscode_insiders
- cu_d15 (.codeium) --supports--> cu_r_vscode_editor
- cu_d16 (.codex) --critical_for--> cu_r_codex_runtime
- cu_d18 (Library/Caches) --disposable--> cuT_system
- cu_d19 (Library/pnpm) --disposable--> cuT_system (with project-dependency check)
- cu_d20 (.Trash) --disposable--> cuT_system
- cu_d17 (.cache/codex-runtimes) --disposable--> cuT_system
- cu_d3 (Library/Containers) --contains--> cu_d3_docker (Docker Desktop state)
- cu_d3_docker --critical_for--> cu_r_docker_engine
- cu_d9 (Pictures) --contains--> cu_d9_photos (user media)
- cu_d10 (projects) --contains--> cu_d10_ai (active project code)
- cu_d1 (App Support) --contains--> cu_d1_cache (rebuildable sub-surface)
- cu_d1_cache --disposable--> cuT_system
- cu_d14 (.local/share/devin) --critical_for--> cu_r_devin_runtime
```

## 4. CU_RUNTIME

```text
- cu_r1: span_hint="Ollama on 127.0.0.1:11434 (PID 864)", meaning="Local model runtime. Models: qwen3, siri, chatgpt, gpt-5.5, minimax. Responds to /api/tags.", role=runtime
- cu_r2: span_hint="FinalAI proxy on 127.0.0.1:50520 (PID 809)", meaning="OpenAI-compatible local proxy. Health 200.", role=runtime
- cu_r3: span_hint="Phoenix on 127.0.0.1:9001 (PID 63375)", meaning="Health/audit bridge. Health 200.", role=runtime
- cu_r4: span_hint="Docker Desktop (com.docker.backend PID 39604)", meaning="Docker engine. VM running. 4 containers active.", role=runtime
- cu_r5: span_hint="redis-server on 127.0.0.1:6379", meaning="Local utility plane.", role=runtime
- cu_r6: span_hint="Postman Agent on 127.0.0.1:10533", meaning="Postman local runtime.", role=runtime
- cu_r7: span_hint="Antigravity IDE on 127.0.0.1:3001 / 23333 / 7779 / 51283 (PID 1155)", meaning="Custom IDE / Electron app with multiple helper processes.", role=runtime
- cu_r8: span_hint="LM Studio (PID 1169) on 127.0.0.1:1234 and 41343", meaning="Local model GUI/runtime.", role=runtime
- cu_r9: span_hint="Pieces OS (PID 18272) on 127.0.0.1:39300 / 50999", meaning="Pieces on-device AI / snippet engine.", role=runtime
- cu_r10: span_hint="agent_os.py on 127.0.0.1:8777 (PID 29819)", meaning="HyperAI agent OS process. Root 200, /openapi.json 200.", role=runtime
- cu_r11: span_hint="apo_gateway.py on 127.0.0.1:9011 (PID 13642)", meaning="APO gateway. Health 200.", role=runtime
- cu_r12: span_hint="hyperai_credentials_service.py on 127.0.0.1:8765 (PID 10357)", meaning="Credentials service. /health not present, process alive.", role=runtime
- cu_r13: span_hint="openapi-servers on 127.0.0.1:8901-8914", meaning="Multiple uvicorn FastAPI services. 8901/8911/8912/8913/8914 openapi.json 200. 8906-8910 not fully probed.", role=runtime
- cu_r14: span_hint="hyperai_os_master.py --daemon (PID 30502)", meaning="HyperAI OS master daemon. No listen port observed.", role=runtime
- cu_r15: span_hint="Code-Server on 127.0.0.1:8080 (PID 4624)", meaning="Browser-based VS Code.", role=runtime
- cu_r16: span_hint="ControlCe on 127.0.0.1:5000", meaning="macOS Control Center listening on port 5000. /health returns 403. This is NOT the expected HyperAI backend.", role=risk
- cu_r17: span_hint="Devin process (PID 10064)", meaning="Current Devin session. pmem 1.6%.", role=runtime
```

## 5. RELATIONS_RUNTIME

```text
- cu_r1 (ollama) --supports--> cuT_local_ai_alive
- cu_r2 (finalai) --supports--> cuT_local_ai_alive
- cu_r3 (phoenix) --supports--> cuT_local_ai_alive
- cu_r4 (docker) --supports--> cuT_local_ai_alive
- cu_r5 (redis) --supports--> cuT_local_utility_plane
- cu_r6 (postman) --supports--> cuT_local_utility_plane
- cu_r7 (antigravity) --supports--> cuT_active_ide
- cu_r8 (lmstudio) --supports--> cuT_active_ide
- cu_r9 (pieces) --supports--> cuT_active_ide
- cu_r10 (agent_os) --supports--> cuT_hyperai_runtime
- cu_r11 (apo_gateway) --supports--> cuT_hyperai_runtime
- cu_r12 (credentials) --supports--> cuT_hyperai_runtime
- cu_r13 (openapi-servers) --supports--> cuT_hyperai_runtime
- cu_r14 (os_master) --supports--> cuT_hyperai_runtime
- cu_r15 (code-server) --supports--> cuT_active_ide
- cu_r16 (ControlCe:5000) --contradicts--> cu_r_backend_port_5000
- cu_r_devin --supports--> cuT_current_session
```

## 6. WHY-CHAIN TABLE (D&R)

| Datum | Why 1 | Why 2 | Endpoint |
|---|---|---|---|
| Data volume 96% full | `Library/` 89G + hidden model dirs (`~/.lmstudio`, `~/.ollama`, `~/.aitk`, `~/.codeium`) | User data, AI models, IDE state not reclaimable without consent | Disk pressure is structural (models + user data), not a transient cache |
| Port 5000 returns 403 | `ControlCe` is bound to port 5000 | macOS Control Center uses 5000 by default | HyperAI backend cannot use 5000 without conflict resolution |
| `.cache/codex-runtimes` 1.5G | Codex runtime cache | Rebuildable after use | Disposable but low impact |
| `Library/Caches` 750M | System/app caches | Can be rebuilt | Safe disposable, but only 750M |
| `docker-recovery` shrunk to 1.3M | Redundant Docker.raw retired | Evidence package retained | Failure fossil reconciled without data loss |

## 7. TOPIC_AND_PLAN

### cuT_disk

**meaning:** Data volume is at 96% capacity. The dominant sources are AI model stores (`.lmstudio` 26G, `.ollama` 17G, `.aitk` 14G, `com.pieces.os` 14G), IDE user data (`.vscode` 11G + 6.8G, VSCodium/Code 10G+), and user media/projects. Rebuildable caches (`Library/Caches`, `.cache`, `.Trash`, `Library/pnpm`) are present but only a few GiB combined.  
**evidence:** [cu_d1, cu_d2, cu_d3, cu_d4, cu_d5, cu_d6, cu_d7, cu_d8, cu_d9, cu_d10, cu_d17, cu_d18, cu_d19, cu_d20, cu_d23]  
**safe:** false (data volume > 90%, structural pressure)  
**risk_reason:** Even after removing 12-24G of Docker.raw backups, the system is still 96% full. Future Docker writes, model downloads, or builds could push it back to 100% and re-trigger the `Docker.raw I/O failure -> VM read-only -> engine death` chain.

### PLAN_DISK

1. **Inspect-only safe cleanup (no risk)**
   - `Library/Caches` (750M) — clear
   - `.cache/codex-runtimes` (1.5G) — clear
   - `.Trash` (292M) — empty
   - `Library/Caches` and app caches inside `Library/Application Support/*/Cache` / `Code Cache` / `CachedData`
   - `Library/com.apple.wallpaper` (822M) — likely cached wallpapers; inspect then clear
   - `Library/WebKit` (116M) / `Library/Safari` (69M) — browser caches; safe
   - Expected yield: **~2-3 GiB**, not enough to reach 90%.

2. **User-data boundary — requires Creator consent**
   - `Pictures` (9.3G), `Library/Mail` (4.6G), `Library/Messages` (99M)
   - `projects` (7.2G), `Archive` (5.1G)
   - `Library/com.pieces.os` (14G), `.lmstudio` (26G), `.ollama` (17G), `.aitk` (14G)
   - `~/.vscode` / `~/.vscode-insiders` / VSCodium user profiles (25G+)
   - These cannot be touched autonomously without value/dependency analysis.

3. **Docker state stability**
   - Continue monitoring `Docker.raw` growth, `vm/init.log` for I/O errors.
   - Keep `HEAVY_WORKLOAD` / `KUBERNETES` denied until data volume < 90%.

### cuT_runtime

**meaning:** Green local AI runtime is mostly healthy. Ollama, FinalAI, Phoenix, Docker, agent_os, apo_gateway, openapi-servers are responsive. One anomaly: port 5000 is occupied by `ControlCe`, not the expected HyperAI backend.  
**evidence:** [cu_r1, cu_r2, cu_r3, cu_r4, cu_r10, cu_r11, cu_r13, cu_r16]  
**safe:** true (all core green services reachable; only non-blocking port conflict)  
**risk_reason:** Port 5000 conflict may break a backend that expects to bind there. `ControlCe` is macOS system UI; moving it requires system-level change or HyperAI backend port reconfiguration.

### PLAN_RUNTIME

1. **Verify ControlCe port 5000**
   - Confirm `ControlCe` is the only listener.
   - Check HyperAI backend intended port (likely `hyperai-user-control-system/backend/server.ts` or `server.js`).
   - If backend expects 5000, reconfigure to another port (e.g., 5052 per AGENTS baseline) or disable Control Center on 5000.

2. **Stabilize service identity matrix**
   - Map every openapi-server (8901-8914) to its role.
   - Verify `agent_os` and `apo_gateway` stay alive after recovery.

3. **Sustained runtime observer**
   - 5-minute observer checking: 9001, 50520, 11434, 8777, 9011, 8901-8914.
   - Alert if any goes down or if Docker I/O errors recur.

## 8. SENSITIVE / PROTECTED ZONES

Do **not** delete or modify without explicit Creator scope:

- `~/.agent_data` (98M) — AI governance / audit data
- `~/.codex` (2.7G) — Codex skills and state
- `~/.continue` (180M) — Continue config
- `~/.agents` (179M) — Devin/AI agents
- `~/.hyperai` (91M) — HyperAI runtime
- `~/.config/hyperai` (24K) — HyperAI credentials/policy
- `~/.config/devin` (52K) — Devin config
- `HyperAI-Sync` (1.1G) — HyperAI canon, memory, tools
- `docker-recovery/evidence-20260729` (1.3M) — Failure fossil
- `~/.ssh`, `~/.gnupg` — identity
- `~/.aws`, `~/.azure`, `~/.gcloud` — cloud credentials

## 9. SAFE DISPOSABLE CANDIDATES (Root_local, inspect-then-clean)

| Target | Estimated | Class | Safety |
|---|---|---|---|
| `~/Library/Caches` | 750M | app cache | high |
| `~/.cache/codex-runtimes` | 1.5G | runtime cache | high |
| `~/.Trash` | 292M | trash | high |
| `~/Library/com.apple.wallpaper` | 822M | wallpaper cache | medium |
| `~/Library/WebKit` / `Safari` | ~185M | browser cache | high |
| `~/Library/Application Support/*/Code Cache` | variable | IDE code cache | medium |
| `~/Library/Application Support/*/CachedData` | variable | IDE cached data | medium |
| `~/Library/Application Support/*/logs` (old) | variable | logs | medium |

**Estimated safe yield: ~2.5–4 GiB** — enough to keep margin but not reach 90%.

## 10. VERDICT

- `STORAGE_PRESSURE_REMAINS` — data volume 96%.
- `SAFE_OPERATING_MARGIN_CREATED` — 19 GiB free > hard floor.
- `RUNTIME_INTEGRITY: MOSTLY_GREEN` — core services reachable.
- `PORT_CONFLICT_5000` — `ControlCe` occupies port 5000.
- `HEAVY_WORKLOAD_ADMISSION: DENIED` until data volume < 90%.
- `DISPOSABLE_CACHE_AVAILABLE` for safe 2-4 GiB cleanup.

## 11. NEXT SINGLE STEP

Choose one:

1. **A. Safe cache cleanup** — I execute the inspect-then-clean list above (no user-data touched). Expected 2-4 GiB.
2. **B. Port 5000 conflict resolution** — I identify which HyperAI backend is supposed to use port 5000 and propose a port change or ControlCe mitigation.
3. **C. Deep model-store audit** — Analyze `.lmstudio`, `.ollama`, `.aitk`, `com.pieces.os` for duplicates / unused models and propose which can be retired.

Hãy nói tôi đi theo A, B, hay C.
