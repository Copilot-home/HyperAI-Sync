# AIOS Factory Reset Recovery Memory - 2026-05-16

Purpose: recover AIOS/Codex mission-router memory after a factory reset.

## Bootstrap Order

1. Restore source repos:
   - `/Users/andy/workbench`
   - `/Users/andy/HyperAI-Sync`
   - `/Users/andy/Documents/MacOSMac`

2. Restore the local skill:
   - source: `/Users/andy/workbench/aios_runtime_orchestrator/restore/hyperai-runtime-orchestrator.SKILL.md`
   - target: `/Users/andy/.agents/skills/hyperai-runtime-orchestrator/SKILL.md`

3. Restore Codex MCP registration:
   - source: `/Users/andy/workbench/aios_runtime_orchestrator/restore/codex-config-aios-mission-router.toml`
   - target config: `/Users/andy/.codex/config.toml`
   - section: `[mcp_servers.AIOS_MISSION_ROUTER]`

4. Restore workspace context:
   - `/Users/andy/Documents/MacOSMac/AGENTS.md`

5. Restart/reload Codex Desktop.

6. Verify:
   - `python3 /Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py verify.run`

## Non-Restored Secrets

These are intentionally excluded:

- `/Users/andy/.codex/auth.json`
- raw API keys
- OAuth tokens
- keychain secrets
- certificate private keys

## Expected Behavior After Restore

AIOS runtime/control missions must route:

`MISSION -> hyperai-runtime-orchestrator -> system-scan-ctx-gam mode=runtime-context -> VERIFY -> QUEUE`

Raw shell may only run after the router returns `allowed_execution_surface`.
