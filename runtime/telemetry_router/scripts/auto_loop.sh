#!/bin/zsh
set -euo pipefail
BASE="/Users/andy/HyperAI-Sync/runtime/telemetry_router"
if ! pgrep -f "docker mcp gateway run --profile ai_coding" >/dev/null 2>&1; then
  docker mcp gateway run --profile ai_coding >> "$BASE/reports/mcp-gateway.log" 2>&1 &
  sleep 2
fi
"$BASE/scripts/apps_inventory.sh" >> "$BASE/reports/launchd.out.log" 2>&1 || true
"$BASE/scripts/codex_tracking.sh" >> "$BASE/reports/launchd.out.log" 2>&1 || true
python3 "$BASE/scripts/router_loop.py" >/dev/null 2>&1 || true
python3 "$BASE/scripts/router_run.py" >/dev/null 2>&1 || true
