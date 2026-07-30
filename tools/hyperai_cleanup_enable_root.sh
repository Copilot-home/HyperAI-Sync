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

A2_SCRIPT="/Users/andy/HyperAI-Sync/tools/hyperai_cleanup_a2.sh"
SUDOERS_FILE="/etc/sudoers.d/hyperai-cleanup"

echo "=== HyperAI cleanup root actuator setup (one-time) ==="

# 1. Ensure A2 script exists and is executable
if [[ ! -x "$A2_SCRIPT" ]]; then
  echo "ERROR: $A2_SCRIPT not found or not executable"
  exit 1
fi

# 2. Add NOPASSWD sudoers entries for controlled cleanup commands
echo "--- writing $SUDOERS_FILE ---"
sudo tee "$SUDOERS_FILE" > /dev/null <<EOF
andy ALL=(root) NOPASSWD: $A2_SCRIPT
EOF
sudo chmod 440 "$SUDOERS_FILE"

# 3. Validate sudoers syntax
echo "--- validating sudoers ---"
sudo visudo -c -f "$SUDOERS_FILE"

# 4. Test NOPASSWD with non-interactive sudo
echo "--- testing NOPASSWD (non-interactive) ---"
sudo -n "$A2_SCRIPT"

echo "=== Setup complete. A2 executed. Future A2 runs can use: sudo $A2_SCRIPT ==="