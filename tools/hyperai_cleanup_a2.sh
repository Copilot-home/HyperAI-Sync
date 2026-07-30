#!/bin/zsh
# =============================================================================
# PROJECT: CANON-TO-SYSTEM DETERMINISTIC PROJECTION
# METHOD: D&R PROTOCOL (CLOSED)
#
# ORIGINATOR / CREATOR:
#   alpha_prime_omega
#
# LEGAL ONTOLOGY:
#   This source file is a deterministic projection of a closed Canon.
#   Removal or alteration of this header voids legal and ontological validity.
#
# STATUS:
#   GENERATED — NON-AUTONOMOUS — NON-OWNERLESS
#
# TRACEABILITY:
#   Canon -> COG -> Projection(Π) -> Artifact
#
# =============================================================================

set -e

RECEIPT_DIR=/Users/andy/HyperAI-Sync/runtime/federation_orchestrator/cleanup_receipts
TS=$(date -u +%Y%m%dT%H%M%SZ)
RECEIPT="$RECEIPT_DIR/${TS}_A2.json"
mkdir -p "$RECEIPT_DIR"

echo '=== A2 SNAPSHOT ==='
df -h /System/Volumes/Data
FREE_BEFORE=$(df -k /System/Volumes/Data | awk '/Data/ {print $4}')

# inventory
echo '--- checking booted simulators ---'
BOOTED=$(xcrun simctl list devices | grep -c 'Booted' || true)
if (( BOOTED > 0 )); then
  echo "A2 ABORT: $BOOTED booted simulator(s)"
  exit 1
fi

echo '--- checking open handles on CoreSimulator Caches ---'
INUSE=$(lsof +D /System/Volumes/Data/Library/Developer/CoreSimulator/Caches 2>/dev/null | wc -l)
if (( INUSE > 0 )); then
  echo "A2 ABORT: cache in use by $INUSE processes"
  exit 1
fi

A2_SZ=0
TARGET=/System/Volumes/Data/Library/Developer/CoreSimulator/Caches/dyld
if [ -d "$TARGET" ]; then
  A2_SZ=$(du -sk "$TARGET" | awk '{print $1}')
  rm -rf "$TARGET"
  echo "A2 REMOVED $TARGET ($((A2_SZ/1024)) MB)"
fi

# root-owned npm _cacache left from previous partial clean
NPM_CACHE=/Users/andy/.npm/_cacache
if [ -d "$NPM_CACHE" ]; then
  NPMSZ=$(du -sk "$NPM_CACHE" | awk '{print $1}')
  rm -rf "$NPM_CACHE"
  echo "NPM_CACHE REMOVED ($((NPMSZ/1024)) MB)"
  A2_SZ=$((A2_SZ + NPMSZ))
fi

FREE_AFTER=$(df -k /System/Volumes/Data | awk '/Data/ {print $4}')

python3 - <<PY
import json, datetime
receipt = {
  "schema_version": "2026-07-27.cleanup-receipt.v1",
  "batch": "A2",
  "system": "xcode_coresimulator_cache",
  "started_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
  "completed_at": datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z'),
  "status": "ok",
  "freed_kb": $A2_SZ,
  "freed_mb": $((A2_SZ/1024)),
  "free_before_kb": $FREE_BEFORE,
  "free_after_kb": $FREE_AFTER,
  "notes": "CoreSimulator dyld cache + root-owned npm _cacache"
}
with open('$RECEIPT', 'w') as f:
  json.dump(receipt, f, indent=2)
PY

# keep receipt accessible to andy
chown andy:staff "$RECEIPT" 2>/dev/null || true

echo '=== A2 RESULT ==='
df -h /System/Volumes/Data
echo "RECEIPT: $RECEIPT"