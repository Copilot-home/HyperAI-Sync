# System Cleanup Audit Trail
Date: 2026-04-27
User: andy

## Phase 1: URL-Encoded Duplicates Deletion
**Timestamp:** [AUTO-FILLED]

### To Delete:
- ~/Library/Application%20Support (2.8M) - verified duplicate of ~/Library/Application Support
- ~/Library/Group%20Containers (3.3M) - verified duplicate of ~/Library/Group Containers

**Reason:** URL-encoded pathnames (space→%20) created duplicate copies. Normal versions are active/maintained.
**Safety:** Confirmed contents already in non-URL-encoded versions.
**Reclaim:** 6.1M

## Phase 2: Desktop Screenshots Archive
**Timestamp:** [AUTO-FILLED]

### To Move:
- ~/Desktop/Ảnh*.png (35 files, 37M)

**Target:** ~/Pictures/Desktop_Screenshots_Archive/
**Reason:** System screenshots should be in Photos app, not Desktop
**Safety:** Preserves originals, merely relocates
**Reclaim:** 37M from Desktop

## Phase 3: APO Tracing Archive
**Timestamp:** [AUTO-FILLED]

### To Archive:
- ~/Desktop/APO_*.{xml,trace,json} (~2M)

**Target:** ~/Archive/APO_traces_2026.tar.gz
**Reason:** Old development/runtime traces, no longer needed
**Safety:** Preserves in tar.gz for future reference
**Reclaim:** ~2M

## Phase 4: Downloads Cleanup
**Timestamp:** [AUTO-FILLED]

### To Delete:
- Old VSIX installers (*.vsix, >30 days)
- DMG files (*.dmg, >30 days)  
- Legacy JSON traces (>100M)

**Reason:** Installation media and old traces
**Safety:** Can be re-downloaded if needed
**Reclaim:** 100-200M

---
**TOTAL EXPECTED RECLAIM: ~156M**
**FINAL DISK EXPECTED: ~394.15Gi/460Gi (86%)**
