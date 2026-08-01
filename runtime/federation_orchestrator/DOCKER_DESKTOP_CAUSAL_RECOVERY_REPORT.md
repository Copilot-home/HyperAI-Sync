# DOCKER DESKTOP CAUSAL RECOVERY REPORT

*Final update: 2026-07-31T12:55:00Z*  
*Recovery execution: docker-recovery-76019c05*  
*Post-recovery probe: docker-probe-74b87127*  
*Sustained observer: 180 s, 6 samples*

## 1. Failure Frame (preserved)

- Execution ID: `docker-probe-7309fec0` (before recovery)
- `/System/Volumes/Data` at **100%** capacity (413 GiB used, ~2.1 GiB free)
- `vm/init.log` contained 14 vda I/O errors:
  - `I/O error, dev vda, sector ...`
  - `JBD2: I/O error when updating journal superblock`
  - `Buffer I/O error on dev vda1`
  - `EXT4-fs (vda1): I/O error while writing superblock`
  - `EXT4-fs (vda1): Remounting filesystem read-only`
- Docker daemon socket (`~/.docker/run/docker.sock`) present but not responsive (`000`)
- `com.docker.backend` and `com.docker.virtualization` processes alive but VM filesystem read-only
- Verdict: `VM_INTERNAL_FAILURE_SUSPECTED`

Preserved artifacts: `docker_recovery_preserved_frame_docker-recovery-fd603f61/`

## 2. Recovery Actions

### Phase 1 — Preserve
Copied the current frame manifest, plane matrix, evidence ledger, hypothesis matrix, and incident sequence to a preservation directory with SHA-256 receipts. `Docker.raw` metadata recorded, not copied (460 GiB logical, 7.1 GiB physical).

### Phase 2 — Create Safe Operating Margin
Reclaimed only rebuildable cache:

| Path | Class | Size before |
|---|---|---|
| `/var/folders/.../T/DockerDesktopUpdates` | Docker Desktop update package cache | 601 MiB |
| `~/Library/Caches/CloudKit` | CloudKit cache | 297 MiB |
| `~/Library/Caches/Homebrew` | Homebrew cache | 22 MiB |
| `~/Library/Caches/com.apple.SpeechRecognitionCore` | Speech cache | 7.4 MiB |
| `~/Library/Caches/com.apple.e5rt.e5bundlecache` | Apple bundle cache | 24 MiB |
| `/var/folders/.../T/CFNetworkDownload_*.tmp` | CFNetwork temp downloads | 6.4 MiB |

Total first-reclaim freed: **756.7 MiB**. Second cleanup freed **27 MiB**.  
Data volume free after first reclaim: **2.9 GiB**.  
Docker.raw physical allocation pre-recovery: **7.1 GiB**; post-recovery: **7.3 GiB**.

### Phase 3 — Controlled Restart

- Attempt 1 (`docker-recovery-fd603f61`):
  - `osascript` quit timed out.
  - `com.docker.backend` (PID 37050) survived SIGTERM.
  - VM did not start; `virtualization=False`.
- Attempt 2 (`docker-recovery-76019c05`):
  - Pre-killed stale backend with SIGTERM, then SIGKILL.
  - `com.docker.backend` and `com.docker.virtualization` both came up after `open -a Docker`.
  - Post-restart process count: 12.

### Phase 4 — Base Engine Validation (post-recovery)

- `docker version`: exit 0
- `docker system info`: exit 0
- `docker ps`: exit 0, 4 containers running
- Socket ping: `200 0.002812`
- Disposable container run: OK
- Container filesystem write: OK
- Container network (ping 8.8.8.8): OK
- BuildKit (`docker buildx ls`): OK
- Host port forwarding: manually verified with `alpine` + `nc` on `127.0.0.1:59999`, returned HTTP 200

## 5. Sustained Validation

Observer: `aios_docker_sustained_observer.py`, 180 s, every 30 s.

- `all_socket_responsive`: **true**
- `all_docker_ps_ok`: **true**
- `all_host_port_forward_ok`: **true**
- `total_new_io_errors`: **0**

## 6. Causal Discrimination

| Hypothesis | Verdict | Rationale |
|---|---|---|
| **H1 HOST_RESOURCE_PRESSURE** | **STRONGLY_SUPPORTED** | vda I/O errors, journal abort, and read-only remount occurred while `/System/Volumes/Data` was 100% full. Recovery required reclaiming margin and a clean restart. VM wrote new blocks once margin was available. |
| **H2 VM_INTERNAL_STATE_FAILURE** | **RECOVERED_CONSEQUENCE** | The EXT4 read-only state was a consequence of write failure, not a persistent Docker.raw defect. A clean restart restored writable state and sustained observation found 0 new I/O errors. |
| **H3 SERVICE_PLANE_BOOT_AMPLIFICATION** | **PARTIAL** | A stale `com.docker.backend` process blocked the first restart and required SIGKILL. This was a process-state obstacle, not a boot-amplification loop. After clearing, Docker started cleanly with 12 processes. |
| **H4 NETWORK_OR_FORWARDING_FAILURE** | **LOW** | Container network and host port forwarding both verified. Docker MCP port 8811 is not active, but that is a separate plane. |

## 7. Final Verdict

**DOCKER_DESKTOP_OPERATIONAL_VERIFIED**

validation_scope = BASE_RUNTIME  
validation_window = 180_SECONDS  
heavy_workload_admission = BLOCKED_BY_STORAGE_PRESSURE  
persistent_storage_safety = NOT_YET_PROVEN

All gates achieved:

- [x] SAFE_OPERATING_MARGIN_CREATED (rebuildable cache reclaimed)
- [x] VM_BOOT_WITHOUT_NEW_IO_ERROR
- [x] ENGINE_DAEMON_RESPONSIVE
- [x] CONTAINER_WRITE_VERIFIED
- [x] CONTAINER_NETWORK_VERIFIED
- [x] HOST_PORT_FORWARDING_VERIFIED
- [x] BUILDKIT_VERIFIED
- [x] SUSTAINED_RESOURCE_BUDGET_RESPECTED (during 180 s observation)
- [x] NO_VM_IO_RECURRENCE

## 8. Storage Sustainability Status

- Data volume `/System/Volumes/Data` is now at **96%** capacity with **~19 GiB free**.
- **SAFE_OPERATING_MARGIN_CREATED**: free space (19 GiB) exceeds hard safety floor (2.7 GiB) and provisional operational target (5 GiB).
- **FAILURE_FOSSIL_RECONCILIATION**: retired `Docker.raw.master` and `Docker.raw.original_at_path` (redundant full-disk copies). Retained `evidence-20260729/` (logs, inspects, version info, hashes, receipt) as minimum forensic package.
- Docker is **operational**, storage pressure is **reduced**, but not yet fully **sustainable** because data volume is still > 90%.
- Heavy workload, Kubernetes, AI inference, and extension ecosystem admission remain **DENIED** until data volume drops below 90%.
- Docker MCP (port 8811) is not active; qualify separately if needed.
- Kubernetes is running inside Docker Desktop but not verified as workload-ready.

## 9. Artifacts

- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_recovery_execution_receipt.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_sustained_validation.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_current_frame_manifest.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_hypothesis_discrimination_matrix.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_plane_state_matrix.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_storage_ledger.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_workload_admission_policy.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_fossil_retention_manifest.json" />
- <ref_file file="/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/docker_recovery_preserved_frame_docker-recovery-fd603f61/preservation_receipt.json" />
