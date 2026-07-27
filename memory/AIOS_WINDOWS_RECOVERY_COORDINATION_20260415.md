# AIOS Windows recovery coordination - 2026-04-15

## Decision

Do not reinstall, reset, purge Docker, or format Windows before preserving AIOS/HyperAI state.

This decision is now bound to the root-host conservation warning:

- `memory/AIOS_ROOT_HOST_CONSERVATION_WARNING_20260415.md`

The current direction is coordinated recovery:

1. keep the filesystem intact
2. preserve a backup manifest
3. let AIOS/federation surfaces record the degraded state
4. repair Windows admin/service authority only after data safety is addressed

## Current measured state

- User-facing PowerShell recovered to `FullLanguage` after restart.
- The Codex-hosted shell still reports profile/constrained-language errors, so Codex commands remain useful for read/write in the workspace but not as proof of the user's fresh PowerShell state.
- Docker Desktop process restart was attempted and completed, but Docker still cannot start its Linux engine.
- Docker/WSL blocker remains:
  - `HCS_E_SERVICE_NOT_AVAILABLE`
  - `vmcompute` stopped
  - `LxssManager` stopped
  - `com.docker.service` stopped
  - service start attempts return access denied from the current non-admin token
- Local admin deadlock remains:
  - `AI\pc` is not an administrator
  - `AI\nguye` and `AI\Administrator` are members of Administrators but disabled
  - `runas` cannot acquire a usable admin credential/token for `AI\nguye`

## AIOS coordination result

- `python tools/hyperai_autonomous_cycle.py` no longer crashes after the runtime policy guard fix.
- Runtime policy now reports:
  - `selected_action = hold_core_degraded`
  - `state_transition = start_managed_runtime_failed`
  - `haios_state = dormant`
  - `boundary_state = recoverable`
  - `operator_attention_required = true`
- Federation orchestrator refresh records:
  - `shell_state.selected_action = hold_core_degraded`
  - `shell_state.haios_state = dormant`

## Code change made for coordination safety

- `tools/hyperai_runtime_policy.py`
  - `summarize_authority()` now handles a missing/null `process` object.
  - Purpose: when Windows/runtime authority is degraded, AIOS can persist a degraded policy state instead of crashing with `AttributeError`.

## Backup posture

Backup manifest:

- `memory/WINDOWS_REINSTALL_BACKUP_MANIFEST_20260415.md`

Only one physical drive is currently visible (`C:`). Root listing reports about 905 GB free, so an internal staging backup is possible, but it is not a real off-device backup.

If internal staging is used, create:

- `C:\AIOS_BACKUP_DO_NOT_DELETE_20260415`

Use only non-destructive copy semantics:

- `robocopy /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /XJ`
- never `/MIR`

## Recovery order

1. Preserve key AIOS/HyperAI folders using the backup manifest.
2. If no external drive is available, use an internal staging folder only as a temporary safety net.
3. Avoid Docker factory reset and Docker data purge.
4. Repair Windows authority:
   - recover or enable an admin account
   - start/repair `vmcompute`, `LxssManager`, and `com.docker.service`
5. Re-run:
   - `wsl -l -v`
   - `docker version`
   - `docker ps`
6. Only after Docker/WSL and admin authority are stable, re-run HyperAI gates.

## Do not do

- Do not wipe Windows.
- Do not format `C:`.
- Do not reset Docker to factory defaults.
- Do not delete `C:\Users\pc`.
- Do not delete root AIOS/HyperAI folders.
- Do not promote stale manifests as live authority.
