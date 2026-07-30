# APΩ UNIFIED STACK — POST-RESTART RECOVERY REPORT

**Executor:** APΩ_UNIFIED_STACK_COMPLETION_EXECUTOR v1.0.0  
**System:** APΩ_HyperAI  
**Mode:** AUTONOMOUS_SYSTEM_ENGINEER  
**Execution Date:** 2026-07-29T09:15:00+00:00  
**State:** DOCKER VM CORRUPTED, LM STUDIO OK, HOST RUNTIME BOUND, V1-V15 PASS

---

## MISSION PACKET

- **User hint:** "nó vừa khởi động lại rồi ... hãy xem cẩn thận ... LM Studio liên quan tới nó".
- **Interpretation:** The user restarted the machine / Docker Desktop. Check LM Studio and Docker carefully.
- **Target surface:** APΩ gateway + 5 OpenAPI tool servers + LM Studio.
- **Risk class:** medium.
- **Approval state:** autonomous.

## SKILL_ROUTING_TABLE

| Skill | Selected | Reason |
|---|---|---|
| `hyperai-runtime-orchestrator` | yes | AIOS mission router for post-restart recovery. |
| Direct shell probes | fallback | Docker skill / reset not available and not approved. |

## EXECUTION_NARRATIVE

### 1. LM Studio Probe

- `lsof -i :1234` found `LM Studio` process listening on `localhost:search-agent` (port 1234).
- Direct `GET http://127.0.0.1:1234/v1/models` with token → **200 OK**, model list returned.
- **Conclusion:** LM Studio healthy after restart.

### 2. Docker Desktop Probe

- `docker ps` showed 4 old `openapi-servers` containers gone (post-restart).
- `docker compose up -d` started 4 containers (time, weather, filesystem, memory) on 8901-8903, 8905.
- `git` container failed to start because the old image lacked the `git` binary (`GitPython` `Bad git executable`).
- `docker compose up -d --build git-server` rebuilt with new `git` binary but failed at commit:
  - `commit failed: write /var/lib/desktop-containerd/daemon/io.containerd.snapshotter.v1.overlayfs/metadata.db: input/output error`
- `docker system prune -f` also failed with:
  - `write /var/lib/desktop-containerd/daemon/io.containerd.metadata.v1.bolt/meta.db: input/output error`
- `docker ps`, `docker logs`, `docker info` all hung or returned I/O errors.
- **Conclusion:** Docker Desktop containerd metadata store is **corrupted**. VM restart did not repair it.

### 3. Docker Container Runtime Check

- 4 containers (time, weather, filesystem, memory) appeared `Up` in `docker ps` for a short time.
- Direct `curl http://127.0.0.1:8901/openapi.json` and `/get_current_utc_time` returned **500 Internal Server Error**.
- `filesystem` returned `Access Denied` with `allowed_directories: ["/nonexistent/tmp"]` (container default, not host).
- **Conclusion:** Docker containers are running but their application layer is not functional; containerd metadata prevents reliable build/run.

### 4. Bounded Mutation — Host Fallback on Alternate Ports

- To avoid killing the broken Docker Desktop process (not approved per `.codex/AGENTS.md`), moved host tool runtime to alternate canonical ports **8801-8805**.
- Created backup `apo_config.20260729T0930Z.yaml`.
- Updated `/Users/andy/.apo/gateway/apo_config.yaml` `tools` section to 8801-8805.
- Started 5 host uvicorn processes:
  - time: 8801
  - weather: 8802
  - filesystem: 8803 (uses `/Users/andy/tmp`)
  - git: 8804
  - memory: 8805
- Restarted APΩ gateway to refresh `httpx.AsyncClient` connection pools.

### 5. End-to-End Verification

- **V1–V15: 15/15 PASS**
- `/v1/models` 200 in **2.47s**.
- LM Studio chat via `apo/lmstudio` **PASS**.
- 5 tool calls **PASS**.
- Filesystem sandbox test **PASS** (`Access Denied` outside `/Users/andy/tmp`).
- GCP controlled proxy **PASS**.
- Secret grep **PASS**.
- Route consistency **PASS** (gateway `/tools` shows 8801-8805).
- Rollback bundles **PASS**.
- Repeat-after-reload **PASS**.
- Bonus: `gpt-5.4` chat via Microsoft Foundry **PASS**.

---

## CANON_DELTA

### Before (post-restart)

- Docker Desktop running but containerd metadata corrupted.
- `apo_config.yaml` tools on 8901-8905 (matching Docker compose, but Docker broken).

### After

- `apo_config.yaml` tools now on **8801-8805** host runtime.
- 5 host uvicorn processes running.
- Full V1-V15 verification passes.
- Docker remains broken with exact evidence captured.

---

## EVIDENCE_LEDGER

- `/Users/andy/HyperAI-Sync/memory/project_state.json`
- `/Users/andy/HyperAI-Sync/memory/APΩ_UNIFIED_STACK_POST_RESTART_20260729T0923Z.md` (this file)
- `/Users/andy/HyperAI-Sync/memory/APΩ_UNIFIED_STACK_DOCKER_ATTEMPT_20260729T0912Z.md`
- `/Users/andy/.apo/gateway/apo_config.yaml`
- `/Users/andy/.apo/gateway/backups/apo_config.20260729T0930Z.yaml`
- `/Users/andy/.apo/gateway/apo_gateway.py`
- `/Users/andy/openapi-servers/compose.yaml`
- `/Users/andy/openapi-servers/servers/git/Dockerfile`
- `/tmp/apo_gateway.log`
- `/tmp/time_server.log`, `/tmp/weather_server.log`, `/tmp/filesystem_server.log`, `/tmp/git_server.log`, `/tmp/memory_server.log`

---

## REMAINING BLOCKERS

1. **Docker Desktop containerd metadata corruption**
   - Evidence: `metadata.db: input/output error` on build, commit, and prune.
   - Required: Docker Desktop factory reset or VM disk repair / reinstall.
   - Not performed: requires explicit approval or manual user action.
2. **Tool port canonical drift**
   - Runtime is on 8801-8805 because Docker holds 8901-8905.
   - Rollback path: repair Docker, stop host tools, restore `apo_config.yaml` to 8901-8905, start `docker compose up -d`.
3. **AGENTS.md / source drift**
   - 12-layer architecture and npm project not yet implemented.

---

## ROLLBACK PATHS

- Restore `/Users/andy/.apo/gateway/apo_config.yaml` from `backups/apo_config.20260729T0930Z.yaml`.
- Kill host uvicorn PIDs for ports 8801-8805.
- Repair Docker Desktop, then `docker compose up -d` to restore 8901-8905.
- Restart APΩ gateway.

---

## FINAL_STATE

- **LM Studio:** healthy, port 1234, token verified.
- **APΩ gateway:** running, all routes reachable.
- **5 OpenAPI tool servers:** running on host ports 8801-8805, all calls pass.
- **GCP proxy:** healthy.
- **Credential broker:** healthy.
- **Docker:** blocked with exact evidence.
- **Ω_global = 1** for the host-runtime branch.
