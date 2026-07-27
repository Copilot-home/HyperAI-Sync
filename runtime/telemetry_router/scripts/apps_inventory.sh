#!/bin/zsh
set -euo pipefail
OUT_DIR="/Users/andy/.codex/worktrees/928e/andy/ops/telemetry-router/reports/apps"
mkdir -p "$OUT_DIR"
TS=$(date +%Y%m%d_%H%M%S)
ALL="$OUT_DIR/apps_inventory_${TS}.txt"
AI="$OUT_DIR/apps_ai_named_${TS}.txt"
AIDEV="$OUT_DIR/apps_ai_dev_runtime_${TS}.txt"
MET="$OUT_DIR/apps_metrics_${TS}.json"

find /Applications -maxdepth 2 -name "*.app" -print | sed 's|/Applications/||' | sort > "$ALL"
find /Applications -maxdepth 2 -iname "*ai*.app" -print | sed 's|/Applications/||' | sort > "$AI"
find /Applications -maxdepth 2 \( -iname "*gpt*.app" -o -iname "*claude*.app" -o -iname "*copilot*.app" -o -iname "*codex*.app" -o -iname "*ollama*.app" -o -iname "*studio*.app" -o -iname "*kiro*.app" -o -iname "*windsurf*.app" -o -iname "*code*.app" -o -iname "*xcode*.app" -o -iname "*debug*.app" -o -iname "*dev*.app" -o -iname "*docker*.app" -o -iname "*terminal*.app" -o -iname "*ssh*.app" \) -print | sed 's|/Applications/||' | sort > "$AIDEV"

app_count=$(wc -l < "$ALL" | tr -d ' ')
ai_named_app_count=$(wc -l < "$AI" | tr -d ' ')
dev_runtime_app_count=$(wc -l < "$AIDEV" | tr -d ' ')

cat > "$MET" <<JSON
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "app_count": $app_count,
  "ai_named_app_count": $ai_named_app_count,
  "dev_runtime_app_count": $dev_runtime_app_count,
  "artifacts": {
    "all": "$ALL",
    "ai_named": "$AI",
    "ai_dev_runtime": "$AIDEV"
  }
}
JSON

ln -sf "$ALL" "$OUT_DIR/latest_apps_inventory.txt"
ln -sf "$AI" "$OUT_DIR/latest_apps_ai_named.txt"
ln -sf "$AIDEV" "$OUT_DIR/latest_apps_ai_dev_runtime.txt"
ln -sf "$MET" "$OUT_DIR/latest_apps_metrics.json"

echo "$MET"
