#!/bin/bash
# Rollback for Gate 1: Materialize Local Root
set -e
ROLLBACK_DIR="/Users/andy/HyperAI-Sync/rollback/gate1_20260730"

echo "Rolling back Gate 1 changes..."

cp "$ROLLBACK_DIR/AGENTS_root.md.bak" /Users/andy/AGENTS.md
cp "$ROLLBACK_DIR/AGENTS_HyperAI-Sync.md.bak" /Users/andy/HyperAI-Sync/AGENTS.md
cp "$ROLLBACK_DIR/AGENTS_codex.md.bak" /Users/andy/.codex/AGENTS.md
cp "$ROLLBACK_DIR/runtime_registry.json.bak" /Users/andy/workbench/aios_runtime_orchestrator/runtime_registry.json
cp "$ROLLBACK_DIR/aios_mission_router.py.bak" /Users/andy/workbench/aios_runtime_orchestrator/aios_mission_router.py

# Unload launchd
launchctl unload ~/Library/LaunchAgents/com.aios.mission.router.plist 2>/dev/null || true
rm -f ~/Library/LaunchAgents/com.aios.mission.router.plist

echo "Rollback complete. Run git diff to inspect."
