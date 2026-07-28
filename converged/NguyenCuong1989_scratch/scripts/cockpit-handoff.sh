#!/bin/bash
# ============================================================
# cockpit-handoff.sh
# Tự động checkpoint WAL + tạo context summary để bắt đầu
# conversation mới mà không mất progress
# ============================================================

CONV_DIR="/Users/andy/.gemini/antigravity/conversations"
HANDOFF_FILE="/Users/andy/.gemini/antigravity/scratch/HANDOFF.md"

echo ""
echo "🚀 Cockpit Handoff Script"
echo "========================="

# --- 1. Checkpoint tất cả WAL files ---
echo ""
echo "📦 Checkpointing WAL files..."
for db in "$CONV_DIR"/*.db; do
  wal="${db}-wal"
  if [ -f "$wal" ] && [ -s "$wal" ]; then
    size=$(du -sh "$wal" | cut -f1)
    echo "  → Checkpointing $(basename "$db") (WAL: $size)..."
    sqlite3 "$db" "PRAGMA wal_checkpoint(TRUNCATE);" 2>/dev/null
    new_size=$(du -sh "$wal" | cut -f1)
    echo "    ✅ Done (WAL: $size → $new_size)"
  fi
done

# --- 2. Tạo handoff summary ---
echo ""
echo "📝 Generating handoff summary..."

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
WORKSPACE="/Users/andy/.gemini/antigravity/scratch"

# Lấy danh sách files đã thay đổi gần đây
RECENT_FILES=$(find "$WORKSPACE" -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -newer "$WORKSPACE/package.json" -type f 2>/dev/null | head -10)

cat > "$HANDOFF_FILE" << EOF
# 🚀 Cockpit Session Handoff
Generated: $TIMESTAMP

## Active Workspace
\`/Users/andy/.gemini/antigravity/scratch\`
Dev server: \`http://localhost:3000\`

## Project: Andy's AI-Powered Workspace Cockpit
Stack: Vanilla HTML + CSS + JS (Vite)

### Current Features (Done ✅)
- 💻 System Diagnostics — real-time env versions
- 📋 Developer Command Toolbox — clipboard copy templates
- 🌿 Git Commit & Merge Hub — 3 tabs (Commit/Merge/Branch)
- 📡 MCP Lazy-load Toggles
- 🕐 Live Clock Widget
- 💡 Quick Tips Panel (slash commands)

### Files
- \`index.html\` — main layout (240 lines)
- \`src/main.js\` — all logic (12KB)
- \`styles/global.css\` — design system

## 📌 Paste này vào conversation mới:
---
\`\`\`
/goal Setup xong môi trường làm việc với Developer Cockpit tại /Users/andy/.gemini/antigravity/scratch, dev server đang chạy tại localhost:3000.
Task tiếp theo: [ĐIỀN TASK Ở ĐÂY]
\`\`\`
---
EOF

echo "  ✅ Handoff file: $HANDOFF_FILE"

# --- 3. Stats ---
echo ""
echo "📊 Conversation DB sizes:"
for db in "$CONV_DIR"/*.db; do
  main_size=$(du -sh "$db" | cut -f1)
  wal="${db}-wal"
  wal_size=$(du -sh "$wal" 2>/dev/null | cut -f1 || echo "0")
  echo "  $(basename "$db"): DB=$main_size | WAL=$wal_size"
done

echo ""
echo "✅ All done! Handoff file saved to:"
echo "   $HANDOFF_FILE"
echo ""
echo "💡 Tip: Mở conversation MỚI trong Antigravity và paste nội dung từ HANDOFF.md"
echo ""
