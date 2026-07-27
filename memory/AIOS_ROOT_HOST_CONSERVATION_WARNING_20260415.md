# AIOS root host conservation warning - 2026-04-15

## Root declaration

This Windows machine is the root host for the current AIOS/HyperAI ecosystem.

The machine is not disposable infrastructure. It contains the active operating memory, local runtimes, tool identities, source lineage, recovery artifacts, and ecosystem coordination state.

## Conservation rule

Preserve the root host before optimizing, repairing, reinstalling, or expanding the ecosystem.

Default stance:

- do not wipe
- do not format
- do not purge Docker
- do not factory-reset Docker Desktop
- do not delete root AIOS/HyperAI folders
- do not treat archive/lineage roots as expendable
- do not assume cloud or repo remotes contain the full operating state

## Hardware limit warning

The current hardware and OS services are finite and already carry many AI/runtime layers. Avoid broad parallel expansion while Windows service authority, Docker/WSL, and admin recovery remain degraded.

Until recovery is complete:

- prefer read-only inventory and memory updates
- prefer local-first proof over new dependency installs
- avoid heavy scans across all backups unless needed for preservation
- avoid starting extra runtimes without a conservation reason
- avoid Docker rebuild/reset workflows

## Root surfaces to conserve

Priority root surfaces include:

- `C:\Users\pc\HyperAI_Phoenix_Master`
- `C:\Users\pc\aidev`
- `C:\Users\pc\AIOS_HyperAI`
- `C:\AI_EMERGENCY_VAULT`
- `C:\AidevGen2`
- `C:\HyperAI`
- `C:\aios_project`
- `C:\AI_Server_Organized`
- `C:\haios-native-dev`
- `C:\Users\pc\.codex`
- `C:\Users\pc\.agents`
- `C:\Users\pc\.ollama`
- `C:\Users\pc\.docker`
- `C:\Users\pc\.ssh`
- editor/operator state under `.vscode*`, `.windsurf`, and related AppData paths

## Current degraded substrate

Known degraded root-host substrate:

- Docker Desktop Linux engine cannot start.
- WSL/HCS path reports `HCS_E_SERVICE_NOT_AVAILABLE`.
- `vmcompute`, `LxssManager`, and `com.docker.service` require admin recovery.
- Current non-admin user cannot start those services.
- Local admin accounts were observed disabled.

## Binding instruction for future cycles

When a future AIOS cycle sees this warning:

1. treat the host as conservation-critical
2. update memory before risky operations
3. prefer backup/staging over reinstall
4. require explicit creator confirmation before reset/reinstall/purge
5. record any recovery action as root-host maintenance, not app-level cleanup

## Sufficient current decision

For now, the key decision is enough:

The machine is the ecosystem root and must be preserved.
