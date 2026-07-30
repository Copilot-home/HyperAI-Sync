# Σ_CTX–GAM System Scan / Runtime-Context + Audit-Global

> Timestamp: 2026-07-27T09:35:00Z
> Baseline: `MACM2_GREEN_LOCAL_BRIDGE_20260710`
> Mode: `runtime-context` + `audit-global`
> Scope: MacM2 local runtime, Devin app, HyperAI green chain, disk pressure

---

## [R1] Runtime / Gate / Health Probes

| Service | Endpoint / Process | Result | Note |
|---------|-------------------|--------|------|
| Phoenix | `http://127.0.0.1:9001/health` | **FAIL** (HTTP 000) | Core green chain offline |
| FinalAI proxy | `http://127.0.0.1:50520/health` | **PASS** (HTTP 200) | PID 50774 listening |
| Ollama | `http://127.0.0.1:11434/api/tags` | **PASS** (HTTP 200) | Expected models present: qwen3-vn-agent-v2, qwen3-vn-clean, qwen3:8b |
| HyperAI credential broker | `http://127.0.0.1:8765` | **PASS** (HTTP 200) | PID 48820, APΩ broker active |
| Titan LAN | `http://192.168.3.158:5052/api/chat/message` | **FAIL** (timeout) | Stale until fresh probe |
| Docker daemon | `docker ps` | **FAIL** (TimeoutExpired after 10s) | Docker Desktop process present (PID 28421) but daemon unresponsive |
| Redis | `127.0.0.1:6379` | LISTEN | Utility plane OK |
| Postman | `127.0.0.1:10533` | LISTEN | Utility plane OK |
| OS Master | `com.hyperai.os.master` | RUNNING (PID 70637) | A0 survival governor |
| FinalAI proxy launchd | `com.hyperai.finalai-openai-proxy` | RUNNING (PID 50774) | Green bridge OK |
| Watchdog / registry dashboard | `com.hyperai.connector.watchdog`, `com.hyperai.registry.dashboard` | exit code 78 | Known WARN pattern, not crash |
| Devin.app | `/Applications/Devin.app` | RUNNING but **remote authority FAIL** | `Failed to resolve remote authority: SSH server closed unexpectedly` / `Failed to initialize configuration service` / `command 'devin.fireProductAnalyticsEvent' not found` |

---

## [B1] Disk Overview

```
Filesystem                     Size   Used  Avail Capacity
/dev/disk3s1 (/System/Volumes/Data)  460Gi  406Gi  7.1Gi   99%
```

Top-level usage (`du -xd 1 /System/Volumes/Data`):

| Path | Size | Role |
|------|------|------|
| `/System/Volumes/Data/Users` | ~272G | user data |
| `/System/Volumes/Data/Applications` | ~63G | apps |
| `/System/Volumes/Data/System` | ~46G | macOS system |
| `/System/Volumes/Data/private` | ~26G | system runtime |
| `/System/Volumes/Data/opt` | ~16G | macOS opt |
| `/System/Volumes/Data/Library` | ~12G | system Library |

Top user directories (`/Users/andy`):

| Path | Size | Role | Risk if touched |
|------|------|------|-----------------|
| `~/Library` | 86G | caches / app data / models / mail | high (contains AI runtime data) |
| `~/Pictures/Photos Library.photoslibrary` | 8.8G | user media | low (user data) |
| `~/projects` | 7.7G | source code repos | high (Canon/project source) |
| `~/Archive` | 5.1G | archive / backup | medium |
| `~/workbench` | 3.6G | workspace | medium |
| `~/Slot-project-local-full` | 3.1G | project | medium |
| `~/micromamba` | 2.3G | conda environments | high (AI runtime) |
| `~/Downloads` | 2.0G | downloads | low |

Largest under `~/Library`:

| Path | Size | Role | Risk |
|------|------|------|------|
| `~/Library/Application Support` | 33G | app caches / extensions / user data | medium |
| `~/Library/Containers/com.docker.docker` | 10G | Docker Desktop data | medium (Docker currently broken) |
| `~/Library/com.pieces.os/production` | 12G | Pieces OS production / local model cache | high (do not delete) |
| `~/Library/Developer` | 9.5G | Xcode / developer tools | medium |
| `~/Library/Application Support/Code` | 6.1G | VS Code user data / caches / extensions | low-medium |
| `~/Library/Application Support/Code - Insiders` | 5.0G | VS Code Insiders data | low-medium |
| `~/Library/Mail` | 4.3G | user mail | low (user data) |

---

## CU_RUNTIME

- `cu_r1`: Devin.app processes alive but renderer logs show `SSH server closed unexpectedly` + `configuration service init failed` — role `runtime` / `risk`
- `cu_r2`: HyperAI credential broker on `:8765` healthy — role `runtime`
- `cu_r3`: FinalAI proxy on `:50520` healthy (HTTP 200) — role `runtime`
- `cu_r4`: Ollama on `:11434` healthy, expected models present — role `model` / `runtime`
- `cu_r5`: Phoenix `:9001` unreachable (HTTP 000) — role `runtime` / `risk`
- `cu_r6`: Docker daemon unresponsive (`docker ps` timeout) — role `runtime` / `risk`
- `cu_r7`: Titan LAN `192.168.3.158:5052` unreachable — role `runtime` / `risk`
- `cu_r8`: `gh` authenticated for `NguyenCuong1989` — role `config`
- `cu_r9`: `/System/Volumes/Data` 99% full — role `risk` (contradicts healthy writes)
- `cu_r10`: `~/.config/devin/config.json` exists with broad allow permissions and no manual-approval gate — role `config` / `risk` (drift from Σ_CTX–GAM canon)
- `cu_r11`: `~/.config/settings.json`, `state.json`, `projects.json` not present — role `config` (expected canon channel missing)
- `cu_r12`: `com.hyperai.os.master` and `com.hyperai.finalai-openai-proxy` launchd agents running — role `runtime`

## RELATIONS_RUNTIME

- `cu_r9 (disk 99%) --critical_for--> cuT_system`
- `cu_r9 (disk 99%) --contradicts--> cuT_runtime_healthy`
- `cu_r5 (Phoenix down) --contradicts--> cuT_green_chain_ready`
- `cu_r6 (Docker unresponsive) --contradicts--> cuT_docker_ready`
- `cu_r1 (Devin remote fail) --contradicts--> cuT_devin_remote_healthy`
- `cu_r4 (Ollama ok) --supports--> cuT_local_ai_alive`
- `cu_r3 (FinalAI ok) --supports--> cuT_local_ai_alive`
- `cu_r2 (broker ok) --supports--> cuT_credential_service_ready`
- `cu_r7 (Titan stale) --contradicts--> cuT_lan_worker_ready`

---

## CU_DISK

- `cu_d1`: `/System/Volumes/Data` 99% full (406G/460G) — role `risk`
- `cu_d2`: `/Users/andy` ~272G — role `data`
- `cu_d3`: `~/Library/Application Support` 33G — role `cache`/`runtime`
- `cu_d4`: `~/Library/Containers/com.docker.docker` 10G — role `cache` (Docker Desktop)
- `cu_d5`: `~/Library/com.pieces.os/production` 12G — role `model` (local model/vector cache, do not delete)
- `cu_d6`: `~/Pictures/Photos Library.photoslibrary` 8.8G — role `data`
- `cu_d7`: `~/projects/AI` 7.7G (DAIOF 6.5G, HyperAI 1.2G) — role `code`
- `cu_d8`: `~/Archive` 5.1G — role `data`
- `cu_d9`: `~/workbench` 3.6G — role `code`
- `cu_d10`: `~/Slot-project-local-full` 3.1G — role `code`
- `cu_d11`: `~/micromamba` 2.3G — role `runtime` (do not delete)
- `cu_d12`: `~/Downloads` 2.0G — role `disposable`
- `cu_d13`: `~/Library/Application Support/Code` 6.1G — role `cache`
- `cu_d14`: `~/Library/Application Support/Code - Insiders` 5.0G — role `cache`

## RELATIONS_DISK

- `cu_d1 (Data 99%) --critical_for--> cuT_system`
- `cu_d1 (Data 99%) --contradicts--> cuT_runtime_healthy`
- `cu_d3 (App Support) --contains--> cu_d13` / `cu_d14`
- `cu_d13 / cu_d14 --disposable--> cuT_system`
- `cu_d5 (Pieces production) --critical_for--> cuT_model_runtime`
- `cu_d7 (projects/AI) --critical_for--> cuT_canon_source_tree`
- `cu_d11 (micromamba) --critical_for--> cuT_python_runtime`
- `cu_d4 (Docker data) --contains--> cu_d1` (contributes to disk pressure)
- `cu_d12 (Downloads) --disposable--> cuT_system`

---

## TOPIC_AND_PLAN

### cuT_disk

- **Meaning**: The Data volume is at 99% capacity. The largest consumers are the user home (`/Users/andy` ~272G), macOS Applications (~63G), and System (~46G). Within `/Users/andy`, `Library/Application Support` (33G), Pieces OS production cache (12G), Docker container data (10G), and project repos (7.7G) dominate.
- **Evidence**: `cu_d1`–`cu_d14`, `df -h`, `du` outputs
- **Safe**: `false` — disk is >98% full
- **Risk reason**: At 99% capacity, config writes, log rotation, Docker operations, and Devin state persistence can fail or hang. Mistaken deletion of `~/.agent_data`, `micromamba/envs`, `models`, or Canon files would break the AI ecosystem.

### PLAN_DISK (inspect-only / needs approval)

1. **Inspect `~/Downloads`** for DMG, ZIP, installers — candidate for deletion.
2. **Inspect `~/Library/Caches`** and `~/Library/Application Support/{Code, Code - Insiders}`** for old extensions, cache, and `Global Storage` artifacts that can be regenerated.
3. **Inspect `~/Library/Containers/com.docker.docker`** for old images/volumes — only if Docker can be started or via `docker system prune` after recovery.
4. **Review `~/Pictures/Photos Library.photoslibrary`** — consider moving to external storage if not needed locally.
5. **Review `~/projects/AI/DAIOF-Framework` (6.5G)** and `~/projects/AI/HyperAI` (1.2G) for `node_modules`, `.venv`, `__pycache__`, build artifacts, and logs that can be cleaned.
6. **Review `~/Archive`, `~/workbench`, `~/Slot-project-local-full`** for duplicates or temporary artifacts.
7. **DO NOT delete**: `~/.agent_data`, `~/.config/hyperai`, `micromamba/envs`, `~/.ollama`, `HyperAI-Sync` Canon/policy files, or any `axis_*` / `models` directories without explicit review.
8. **Re-verify**: run `df -h` after cleanup; target >10% free on `/System/Volumes/Data`.

### cuT_runtime

- **Meaning**: Local AI green chain is **partially healthy**: FinalAI proxy (`:50520`), Ollama (`:11434`), and the new HyperAI credential broker (`:8765`) are live. Phoenix (`:9001`) is offline, Docker is unresponsive, and Devin.app cannot resolve its remote SSH authority. Disk pressure is a common local stressor that explains configuration-service and Docker failures.
- **Evidence**: `cu_r1`–`cu_r12`, health probes, `launchctl list`
- **Safe**: `false`
- **Risk reason**: Core green chain incomplete (Phoenix FAIL); Docker cannot spawn containers; Devin IDE remote workspace disconnected. These block containerized deployment and IDE-driven remote work.

### PLAN_RUNTIME (inspect-only / needs approval)

1. **Free disk space first**; then retest `docker ps` and Devin configuration init.
2. **Probe Phoenix**: check if `com.hyperai.phoenix` launchd exists; review logs under `~/Library/Logs` or `runtime/federation_orchestrator`.
3. **Check remote SSH host** for Devin: verify network, remote host status, and SSH credentials (this is external to the local machine and may need user/cloud action).
4. **Restart Devin.app** only after disk cleanup and remote-host verification (user approval required).
5. **Re-run full health probes** and `python tools/hyperai_ooda_loop.py --once` to confirm green chain closure.

---

## [A1-A4] D&R Audit-Global — Devin Error Cluster

### I. Deconstruction

- **A. Context groups**: Devin.app (Electron/VS Code fork), local MacM2, remote SSH workspace, HyperAI green chain, disk/storage.
- **B. Causal dependencies**:
  - Devin app needs local configuration service writes to `~/Library/Application Support/Devin`.
  - Devin remote authority needs reachable SSH server and valid auth.
  - Docker daemon needs disk space for image/container operations.
  - Phoenix audit bridge needs local process/port/health.
- **C. Thesis**: The observed symptom cluster is best explained by **two independent breakpoints** that are amplified by a common stressor (disk pressure): a remote SSH authority failure in Devin, and local write/service instability caused by a 99%-full Data volume.
- **D. Facts**: `df` 99%; `docker ps` timeout; Phoenix `:9001` 000; Devin logs show remote authority closed and config init failed.
- **E. GAM anti-drift vs baseline**: Baseline expects Phoenix `:9001` LIVE, FinalAI `:50520` 200, Ollama `:11434` 200. Current: Phoenix FAIL, Docker unresponsive, Devin remote FAIL.

### II. Focal Point

`focal = (Devin remote authority FAIL + config init FAIL + Docker freeze + Phoenix down) <- disk pressure & remote host closure`

### III. Re-architecture / Optimization

- **Disk**: Implement periodic `df` check and safe cleanup automation (cache, Downloads, Docker prune) gated by user approval.
- **Runtime**: Add a `green-chain` watchdog that probes Phoenix/FinalAI/Ollama/credential-broker and records `cuT_runtime` state on every OODA cycle.
- **Devin remote**: Document the remote workspace/SSH host and credentials outside the local runtime; treat as external gate.

---

## WHY_CHAIN_TABLE

| Datum | Why chain | Endpoint |
|-------|-------------|----------|
| `Failed to initialize configuration service` | why? config write/read may fail on 99% full disk → why? `/System/Volumes/Data` has only 7.1G free (406G/460G) → endpoint: free disk or move storage |
| `Failed to resolve remote authority: SSH server closed unexpectedly` | why? Devin cannot connect to remote host SSH server → why? remote host closed connection / network issue / auth failure → endpoint: verify remote host/network/credentials |
| `docker ps` times out | why? Docker daemon unresponsive → why? disk full plus 10G Docker container data may cause daemon I/O stalls → endpoint: free disk, then restart Docker daemon |
| Phoenix `:9001` unreachable | why? Phoenix service not listening → why? process not running or launchd not loaded → endpoint: inspect Phoenix launchd/logs and start if intended |
| `command 'devin.fireProductAnalyticsEvent' not found` | why? Devin extension did not activate → why? remote authority/config init failed earlier → endpoint: resolve remote/config first, then reload Devin window |

---

## GLOBAL_CONCLUSION

- **runtime_integrity**: `PARTIAL` — FinalAI, Ollama, HyperAI credential broker OK; Phoenix offline; Docker unresponsive; Devin remote authority failed.
- **reachability**: `PARTIAL` — local `:50520`, `:11434`, `:8765` reachable; `:9001` and Titan LAN and Docker daemon unreachable.
- **global_breakpoint**: **Disk pressure** is the local breakpoint (`/System/Volumes/Data` 99%). **Remote SSH server closure** is an external breakpoint requiring user/cloud verification.
- **Overall**: `PARTIAL / FAIL` — do not proceed with write-heavy or containerized actions until disk is freed and the remote host is reachable.
