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
"""Apply APO/Canon environment anchors to all AI and dev-tool runtime surfaces.

Idempotent: only adds env/anchors/symlinks; never deletes or modifies app data.
"""

import datetime
import os
import re
import subprocess
import sys
from pathlib import Path


HOME = Path.home()
CANON_ROOT = HOME / "axcontrol"
APPLY_CANON_SH = CANON_ROOT / "scripts" / "apply-global-canon.sh"
LOAD_CANON_SH = CANON_ROOT / "scripts" / "load-canon-env.sh"
ENV_FILE = HOME / ".config" / "axcanon" / "global.env"
CANON_MEMORY = HOME / ".axcanon" / "memory"

# Shell rc files to source global.env in.
SHELL_RCS = [
    HOME / ".zshenv",
    HOME / ".zshrc",
    HOME / ".zprofile",
    HOME / ".bashrc",
    HOME / ".bash_profile",
]

# Extra lab directories beyond the base list in apply-global-canon.sh.
# Patterns are relative to $HOME. Only existing directories get canon symlinks.
LAB_PATTERNS = [
    ".antigravity*",
    ".antigravity-ide",
    ".claude*",
    ".codex*",
    ".codexbar",
    ".cursor",
    ".devin",
    ".config/devin",
    ".hyper*",
    ".aitk",
    ".aider-desk",
    ".kombai*",
    ".sema4ai",
    ".next-devtools-mcp",
    ".wallaby",
    ".dbtools",
    ".sqlcontainers",
    ".altestrunner",
    ".ai-*",
    ".aios",
    ".daiof",
    ".vscode",
    ".vscode-insiders",
    ".vscode*",
    "HyperAI*",
    "hypernode-runtime",
    "ai-lab",
    "gke-ai-agent-lab",
    "my_too_test",
    "DAIOF*",
    "daiof-*",
    "multi-container-app",
    "testcontainers-cloud-java-example",
    "ollama-test",
    "tests",
    "XcodeSourceEditorExtension-Alignment",
    "vscode-*",
    "aws-toolkit-vscode",
    "tools",
]


EXCLUDED_NAMES = {
    ".", "..", ".Trash", ".axcanon", "axcontrol", "Library", "Applications",
}


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_canon_env():
    """Run the canonical load script to write global.env and launchctl setenv."""
    print(f"[run] {LOAD_CANON_SH}")
    result = subprocess.run([str(LOAD_CANON_SH)], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)


def source_env_in_current_shell():
    """Source global.env in the current process environment."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line.startswith("export "):
            continue
        line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"')
        os.environ[key] = value


def ensure_shell_rc_sources():
    """Add global.env source line to shell rc files (idempotent)."""
    source_line = 'if [ -f "$HOME/.config/axcanon/global.env" ]; then . "$HOME/.config/axcanon/global.env"; fi'
    for rc in SHELL_RCS:
        rc.touch(exist_ok=True)
        text = rc.read_text()
        if source_line in text:
            continue
        with open(rc, "a") as f:
            f.write("\n# APO/Canon global environment\n" + source_line + "\n")


def run_apply_global_canon():
    """Run the base apply script."""
    print(f"[run] {APPLY_CANON_SH}")
    result = subprocess.run([str(APPLY_CANON_SH)], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)


def discover_extra_labs() -> set[Path]:
    """Expand lab patterns and filter to existing directories."""
    labs = set()
    for pat in LAB_PATTERNS:
        for p in HOME.glob(pat):
            if p.is_dir() and not p.is_symlink():
                if p.name in EXCLUDED_NAMES:
                    continue
                if p == CANON_ROOT or p == CANON_MEMORY or p == HOME:
                    continue
                labs.add(p.resolve())
    return labs


def ensure_canon_symlinks(lab_dir: Path):
    """Create .canon_root and .canon_env symlinks inside a lab directory."""
    root_link = lab_dir / ".canon_root"
    env_link = lab_dir / ".canon_env"

    if root_link.exists() or root_link.is_symlink():
        try:
            if os.readlink(root_link) != str(CANON_ROOT):
                root_link.unlink()
        except Exception:
            pass
    if not root_link.exists() and not root_link.is_symlink():
        root_link.symlink_to(CANON_ROOT, target_is_directory=True)

    if env_link.exists() or env_link.is_symlink():
        try:
            if os.readlink(env_link) != str(ENV_FILE):
                env_link.unlink()
        except Exception:
            pass
    if not env_link.exists() and not env_link.is_symlink():
        env_link.symlink_to(ENV_FILE)


def set_launchctl_env():
    """Set all AX_* variables via launchctl for GUI/app visibility."""
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line.startswith("export "):
            continue
        line = line[7:].strip()
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"')
        subprocess.run(["launchctl", "setenv", key, value], capture_output=True)


def write_checkpoint():
    CANON_MEMORY.mkdir(parents=True, exist_ok=True)
    brain = CANON_MEMORY / "brain.index"
    with open(brain, "a") as f:
        f.write(f"{now_iso()} hyperai_canon_apply: environment and anchors applied\n")


def verify() -> dict:
    """Verify env and symlinks."""
    results = {
        "env_file_exists": ENV_FILE.exists(),
        "env_vars": {},
        "launchctl_vars": {},
        "symlink_count": 0,
        "lab_dirs": 0,
    }
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line.startswith("export ") and "=" in line:
                kv = line[7:]
                key, _, value = kv.partition("=")
                results["env_vars"][key] = value.strip().strip('"')

    # Check launchctl env for known keys
    for key in results["env_vars"]:
        try:
            out = subprocess.run(["launchctl", "getenv", key], capture_output=True, text=True).stdout.strip()
            results["launchctl_vars"][key] = out
        except Exception:
            results["launchctl_vars"][key] = "ERROR"

    for pat in LAB_PATTERNS:
        for p in HOME.glob(pat):
            if p.is_dir() and (p / ".canon_root").is_symlink() and (p / ".canon_env").is_symlink():
                results["symlink_count"] += 2
                results["lab_dirs"] += 1

    return results


def main():
    print(f"=== APO/Canon environment apply started at {now_iso()} ===")

    # 1. Ensure the canonical env file is up-to-date and in current shell.
    ensure_canon_env()
    source_env_in_current_shell()

    # 2. Base apply: sets launch agent, rc files, base lab symlinks.
    run_apply_global_canon()

    # 3. Ensure all shell rc files source global.env.
    ensure_shell_rc_sources()

    # 4. Discover and anchor all extra labs.
    extra_labs = discover_extra_labs()
    for lab in sorted(extra_labs):
        ensure_canon_symlinks(lab)

    # 5. Push variables to launchctl for GUI/app processes.
    set_launchctl_env()

    # 6. Checkpoint.
    write_checkpoint()

    # 7. Verify and report.
    results = verify()
    print("\n=== APO/Canon environment applied ===")
    print(f"Env file:          {ENV_FILE}")
    print(f"AX_* variables:    {len(results['env_vars'])}")
    for k, v in results["env_vars"].items():
        print(f"  {k}={v}")
    print(f"Launchctl get env: {len(results['launchctl_vars'])} keys")
    print(f"Lab dirs anchored: {results['lab_dirs']}")
    print(f"Canon symlinks:    {results['symlink_count']}")
    print(f"Checkpoint:        {CANON_MEMORY / 'brain.index'}")

    # Print shell hint
    print("\nTo load in current shell:")
    print("  source ~/.config/axcanon/global.env")


if __name__ == "__main__":
    main()
