#!/bin/zsh
set -euo pipefail
BASE="/Users/andy/HyperAI-Sync/runtime/telemetry_router"
OUT="$BASE/reports/codex"
mkdir -p "$OUT"
TS=$(date +%Y%m%d_%H%M%S)
RAW="$OUT/codex_tracking_${TS}.txt"
MET="$OUT/codex_metrics_${TS}.json"
latest_codex_log="/Users/andy/.codex/log/codex-tui.log"
latest_vscode=$(ls -1t ~/Library/Application\ Support/Code/logs 2>/dev/null | head -n1 || true)
{
  echo "ts=$TS"
  echo "--- codex home ---"
  du -sh /Users/andy/.codex 2>/dev/null || true
  echo "--- codex sessions ---"
  find /Users/andy/.codex/sessions -type f 2>/dev/null | wc -l
  echo "--- codex warnings/errors ---"
  rg -n "WARN|ERROR|MCP error|Connection closed|insufficient_quota|rate_limit|invalid_api_key" "$latest_codex_log" 2>/dev/null | tail -n 120 || true
  echo "--- vscode codex mcp ---"
  if [ -n "$latest_vscode" ]; then
    rg -n "CodexMcpConnection|openai.chatgpt|mcpServer.*MCP_DOCKER|mcpServer" ~/Library/Application\ Support/Code/logs/$latest_vscode -g '*.log' 2>/dev/null | head -n 200 || true
  fi
} > "$RAW"
warn_count=$( (rg -n "WARN|ERROR" "$latest_codex_log" 2>/dev/null || true) | wc -l | tr -d ' ')
mcp_err_count=$( (rg -n "MCP error|Connection closed" "$latest_codex_log" 2>/dev/null || true) | wc -l | tr -d ' ')
session_files=$(find /Users/andy/.codex/sessions -type f 2>/dev/null | wc -l | tr -d ' ')
cat > "$MET" <<JSON
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "codex_warn_error_count": $warn_count,
  "codex_mcp_error_markers": $mcp_err_count,
  "codex_session_files": $session_files,
  "raw_report": "$RAW"
}
JSON
ln -sf "$RAW" "$OUT/latest_codex_tracking.txt"
ln -sf "$MET" "$OUT/latest_codex_metrics.json"
echo "$MET"
