#!/usr/bin/env python3
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
"""Collect APO/Canon documents, apply canonical headers, and re-standardize.

- Adds CANONICAL_CODEGEN_LAW.md header to HyperAI-Sync/tools source files.
- Creates /Users/andy/axcontrol/canon/apo/ as the common APO canon library.
- Mirrors the library into ~/.axcanon/memory/apo_canon.
- Hardlinks all known APO/Canon artifacts into the library.
- Re-runs hyperai_apo_standardize.py so the bundle anchors to the common canon.
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Adjust sys.path so we can import from hyperai_apo_standardize.
TOOLS = Path("/Users/andy/HyperAI-Sync/tools")
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import hyperai_apo_standardize as apo


# Canonical codegen header from /Users/andy/axcontrol/CANONICAL_CODEGEN_LAW.md.
CANON_HEADER = """# =============================================================================
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
"""

HEADER_MARKER = "CANON-TO-SYSTEM DETERMINISTIC PROJECTION"

HOME = Path("/Users/andy")
CANON_ROOT = HOME / "axcontrol"
CANON_APO_DIR = CANON_ROOT / "canon" / "apo"
CANON_MEMORY_LINK = HOME / ".axcanon" / "memory" / "apo_canon"
TOOLS_DIR = HOME / "HyperAI-Sync" / "tools"

APO_SOURCES = [
    # APO technical canon (Downloads)
    HOME / "Downloads" / "APO_LOCK_LAYER.md",
    HOME / "Downloads" / "APO_FULL_NOTARY.py",
    HOME / "Downloads" / "APO_MULTI_MERKLE.py",
    HOME / "Downloads" / "APO_FULL_PROOF.json",
    HOME / "Downloads" / "APO_LOCK_LAYER.proof.json",
    HOME / "Downloads" / "APO_MERKLE_WAL.json",

    # AXCONTROL global canon
    CANON_ROOT / "CANONICAL_CODEGEN_LAW.md",
    CANON_ROOT / "docs" / "OPS_GLOBAL_CANON.md",
    CANON_ROOT / "docs" / "Sigma_APO_Operational_Canon.md",
    CANON_ROOT / "docs" / "Sigma_APO_Sleep_Workflow.md",
    CANON_ROOT / "docs" / "Sigma_APO_NotebookLM_ModeA.md",
    CANON_ROOT / "scripts" / "apply-global-canon.sh",
    CANON_ROOT / "scripts" / "load-canon-env.sh",

    # Σ_APΩ–COS runtime evidence
    HOME / "my_too_test" / "sigma-cos" / "README.md",
    HOME / "my_too_test" / "sigma-cos" / "formal" / "runtime.py",
    HOME / "my_too_test" / "sigma-cos" / "diagrams" / "architecture.mmd",
    HOME / "my_too_test" / "sigma-cos" / "diagrams" / "architecture.puml",
    HOME / "my_too_test" / "sigma-cos" / "tests" / "smoke.sh",
    HOME / "my_too_test" / ".github" / "scripts" / "autonomous_developer.py",

    # AIOS/HyperAI memory canons
    HOME / "HyperAI-Sync" / "memory" / "AIOS_CLEANUP_CANON.md",
    HOME / "HyperAI-Sync" / "memory" / "APΩ_CREDENTIAL_CANON.md",
    HOME / "HyperAI-Sync" / "memory" / "AIOS_CREATOR_ROLE_SUPERPOSITION_PROTOCOL.md",
    HOME / "HyperAI-Sync" / "memory" / "AIOS_CREATOR_AI_COEXISTENCE_WORKFLOW.md",
    HOME / "HyperAI-Sync" / "memory" / "AIOS_APP_RUNTIME_RESPONSIBILITY_AUDIT_20260415.md",
    HOME / "HyperAI-Sync" / "memory" / "AIOS_GCP_CLOUD_SUBSTRATE_OBSERVATION_20260415.md",
    HOME / "HyperAI-Sync" / "memory" / "APPLE_NATIVE_EVOLUTION_PROBE_ANALYSIS_20260727.md",
    HOME / "HyperAI-Sync" / "memory" / "agent6_synthesis_capsule.md",
    HOME / "HyperAI-Sync" / "memory" / "NotebookLM_Integration_Protocol.md",
    HOME / "HyperAI-Sync" / "memory" / "NotebookLM_Mind_Map_Research.md",
    HOME / "HyperAI-Sync" / "memory" / "NotebookLM_Enterprise_API_Probe.md",
    HOME / "HyperAI-Sync" / "memory" / "Sigma_APO_Complete_System_Documentation.md",

    # HyperAI cleanup surface
    HOME / "HyperAI-Sync" / ".devin" / "skills" / "system-cleanup-executor" / "SKILL.md",
    HOME / "HyperAI-Sync" / "tools" / "hyperai_cleanup_executor.py",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def has_canon_header(path: Path) -> bool:
    try:
        text = path.read_text()
    except Exception:
        return False
    # Skip shebang for the check.
    lines = text.splitlines()
    for line in lines[:3]:
        if line.startswith("#!"):
            lines = lines[1:]
            break
    joined = "\n".join(lines[:20])
    return HEADER_MARKER in joined


def add_canon_header(path: Path):
    if has_canon_header(path):
        return False
    try:
        text = path.read_text()
    except Exception:
        return False
    lines = text.splitlines()
    shebang = ""
    if lines and lines[0].startswith("#!"):
        shebang = lines[0] + "\n"
        rest = "\n".join(lines[1:])
    else:
        rest = "\n".join(lines)
    if rest and not rest.startswith("\n"):
        rest = "\n" + rest
    new_text = shebang + CANON_HEADER + rest
    path.write_text(new_text)
    return True


def hardlink_or_copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        try:
            if os.path.samefile(src, dst):
                return
        except Exception:
            pass
        # Common folder is under our control; replace to keep idempotent.
        os.unlink(dst)
    try:
        os.link(src, dst)
    except OSError:
        # Fall back to copy if hardlink fails (different fs, permissions, etc.).
        import shutil
        shutil.copy2(src, dst)


def relative_to_home(path: Path) -> Path:
    return path.relative_to(HOME)


def main():
    created_at = now_iso()

    # 1. Add canonical headers to all HyperAI-Sync/tools source files.
    header_count = 0
    for path in sorted(TOOLS_DIR.iterdir()):
        if not path.is_file():
            continue
        if path.suffix not in (".py", ".sh"):
            continue
        if path.name.startswith("__"):
            continue
        if add_canon_header(path):
            header_count += 1
    print(f"[canon header] applied to {header_count} files in {TOOLS_DIR}")

    # 2. Create common APO canon library.
    CANON_APO_DIR.mkdir(parents=True, exist_ok=True)

    # 3. Mirror into common canon memory.
    CANON_MEMORY_LINK.parent.mkdir(parents=True, exist_ok=True)
    if CANON_MEMORY_LINK.is_symlink() or CANON_MEMORY_LINK.exists():
        if CANON_MEMORY_LINK.is_symlink() and os.readlink(CANON_MEMORY_LINK) == str(CANON_APO_DIR):
            pass
        else:
            CANON_MEMORY_LINK.unlink()
            CANON_MEMORY_LINK.symlink_to(CANON_APO_DIR, target_is_directory=True)
    else:
        CANON_MEMORY_LINK.symlink_to(CANON_APO_DIR, target_is_directory=True)

    # 4. Hardlink APO/Canon sources into the library, preserving relative paths.
    index_entries = []
    for src in APO_SOURCES:
        if not src.exists():
            print(f"[warn] missing APO source: {src}")
            continue
        rel = relative_to_home(src)
        dst = CANON_APO_DIR / rel
        hardlink_or_copy(src, dst)
        canon_bytes, canon_hash, raw_size = apo.canonicalize_file(dst)
        has_header = has_canon_header(dst) if dst.suffix in (".py", ".sh") else None
        index_entries.append({
            "source_path": str(src),
            "canon_path": str(dst),
            "relative_path": str(rel),
            "size_bytes": raw_size,
            "canonical_hash": canon_hash,
            "has_canon_header": has_header,
        })

    # 5. Re-run APO standardization so the bundle uses the common canon library.
    print("[run] hyperai_apo_standardize.py")
    result = subprocess.run(
        [sys.executable, str(TOOLS_DIR / "hyperai_apo_standardize.py")],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

    # 6. Read the freshly generated index for the final report.
    bundle_index_path = HOME / "HyperAI-Sync" / "runtime" / "federation_orchestrator" / "cleanup_receipts" / "APO_cleanup_index.json"
    bundle_index = json.loads(bundle_index_path.read_text()) if bundle_index_path.exists() else {}

    # 7. Write the APO canon library index.
    canon_index = {
        "schema_version": "APO_CANON_LIBRARY_V1",
        "created_at_utc": created_at,
        "canon_root": str(CANON_APO_DIR),
        "canon_memory_link": str(CANON_MEMORY_LINK),
        "artifact_count": len(index_entries),
        "bundle_index": bundle_index,
        "artifacts": index_entries,
    }
    index_path = CANON_APO_DIR / "APO_CANON_INDEX.json"
    index_path.write_text(json.dumps(canon_index, indent=2, sort_keys=True, ensure_ascii=False))

    # 8. Final stats.
    files_with_header = sum(1 for e in index_entries if e["has_canon_header"] is True)
    files_without_header = sum(1 for e in index_entries if e["has_canon_header"] is False)
    print(f"[APO canon library] {CANON_APO_DIR}")
    print(f"[APO canon memory ] {CANON_MEMORY_LINK}")
    print(f"[APO sources      ] {len(index_entries)} artifacts")
    print(f"[header ok        ] {files_with_header}")
    print(f"[header missing   ] {files_without_header}")
    print(f"[canon index      ] {index_path}")
    print(f"[bundle index     ] {bundle_index_path}")


if __name__ == "__main__":
    main()
