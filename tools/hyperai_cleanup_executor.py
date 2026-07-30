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

"""HyperAI system cleanup executor.

Reads AIOS_CLEANUP_CANON.md and executes per-system cleanup recipes.
Produces JSON receipts and respects DO_NOT_DELETE / protected anchors.

Dry-run mode only inspects and estimates; it never purges caches or deletes files.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANON_PATH = ROOT / "memory" / "AIOS_CLEANUP_CANON.md"
RECEIPT_DIR = ROOT / "runtime" / "federation_orchestrator" / "cleanup_receipts"

HOME = Path.home()

# Paths that must never be deleted as directories or prefixes.
PROTECTED_PREFIXES = [
    str(HOME / ".hyperai"),
    str(HOME / ".codex"),
    str(HOME / ".config" / "devin"),
    str(HOME / ".ssh"),
    str(HOME / ".gnupg"),
    str(HOME / ".ollama" / "models"),
    str(ROOT),
    str(HOME / "Pictures" / "Photos Library.photoslibrary"),
]

# Patterns that must never be deleted.
PROTECTED_PATTERNS = [
    "*private*",
    "*key*",
    "*credential*",
    "*wallet*",
    "*secret*",
    "*token*",
    "*password*",
    "*passphrase*",
    "APO_*",
    "*.git",
    "*.photoslibrary",
]

# Allowed leaf directory names to delete even if inside a project.
DISPOSABLE_LEAVES = {
    "__pycache__",
    ".pytest_cache",
    "CachedExtensionVSIXs",
    "Crashpad",
    "logs",
    "Cache",
    "CachedData",
    "CachedProfilesData",
    "DerivedData",
    "in_progress",  # Docker install leftover
    ".DS_Store",
    "node_modules",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def disk_free_mb(path: str = "/System/Volumes/Data") -> int:
    try:
        p = subprocess.run(
            ["df", "-k", path],
            capture_output=True,
            text=True,
            timeout=5,
            check=True,
        )
        lines = p.stdout.splitlines()
        if len(lines) < 2:
            return -1
        return int(lines[1].split()[3]) // 1024
    except Exception:
        return -1


def is_protected(path: Path) -> bool:
    spath = str(path.resolve())
    for prefix in PROTECTED_PREFIXES:
        if spath == prefix or spath.startswith(prefix + os.sep):
            # Allow specific disposable leaves inside protected roots.
            if path.name in DISPOSABLE_LEAVES:
                return False
            return True
    for pat in PROTECTED_PATTERNS:
        if fnmatch.fnmatch(path.name.lower(), pat.lower()):
            return True
    return False


def path_size_mb(path: Path) -> float:
    if not path.exists():
        return 0.0
    try:
        p = subprocess.run(
            ["du", "-sk", str(path)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if p.returncode == 0:
            return int(p.stdout.split()[0]) / 1024.0
    except Exception:
        pass
    return 0.0


def safe_delete(target: Path, dry_run: bool = False) -> dict[str, Any]:
    """Delete a file or directory if safe. Returns action metadata."""
    action = {
        "path": str(target),
        "status": "skipped",
        "reason": None,
        "dry_run": dry_run,
        "estimated_mb": path_size_mb(target),
    }
    if not target.exists():
        action["status"] = "missing"
        action["estimated_mb"] = 0.0
        return action
    if is_protected(target):
        action["status"] = "protected"
        action["reason"] = "DO_NOT_DELETE"
        return action
    if dry_run:
        action["status"] = "dry_run"
        return action
    def _make_writable(path: Path) -> None:
        try:
            if path.is_dir():
                for root, dirs, files in os.walk(path):
                    for d in dirs:
                        p = Path(root) / d
                        p.chmod(p.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
                    for f in files:
                        p = Path(root) / f
                        p.chmod(p.stat().st_mode | stat.S_IWUSR)
            else:
                target.chmod(target.stat().st_mode | stat.S_IWUSR)
        except Exception:
            pass

    try:
        if target.is_dir():
            _make_writable(target)
            shutil.rmtree(target)
        else:
            _make_writable(target)
            target.unlink()
        action["status"] = "deleted"
    except Exception as e:
        action["status"] = "error"
        action["reason"] = f"{type(e).__name__}: {e}"
    return action


def run_command(
    cmd: list[str],
    timeout: int = 60,
    cwd: Path | None = None,
) -> tuple[int, str, str]:
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd) if cwd else None,
        )
        return p.returncode, p.stdout, p.stderr
    except Exception as e:
        return 1, "", f"{type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Helpers for cache directory discovery and dry-run estimation
# ---------------------------------------------------------------------------


def get_cache_dir(tool: str) -> Path | None:
    """Return the cache directory for pip/npm/pnpm/yarn or None."""
    cmds: dict[str, list[str]] = {
        "pip": [sys.executable, "-m", "pip", "cache", "dir"],
        "npm": ["npm", "config", "get", "cache"],
        "pnpm": ["pnpm", "store", "path"],
        "yarn": ["yarn", "cache", "dir"],
    }
    if tool not in cmds or not shutil.which(tool if tool != "pip" else sys.executable):
        return None
    rc, out, _ = run_command(cmds[tool], timeout=20)
    if rc != 0:
        return None
    path_text = out.strip().splitlines()[0].strip()
    if not path_text:
        return None
    p = Path(path_text).expanduser()
    return p if p.exists() else None


def _add_cache_estimate(actions: list[dict[str, Any]], tool: str, path: Path | None) -> None:
    if path and path.exists():
        actions.append({
            "command": f"{tool} cache clean/purge (estimated)",
            "status": "dry_run",
            "estimated_mb": path_size_mb(path),
            "path": str(path),
        })


def find_matching_paths(root: Path, names: set[str]) -> list[Path]:
    if not root.exists():
        return []
    paths: list[Path] = []
    for name in names:
        paths.extend(root.rglob(name))
    return paths


# ---------------------------------------------------------------------------
# Per-system recipes
# ---------------------------------------------------------------------------


def recipe_pip(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []

    if dry_run:
        pip_cache = get_cache_dir("pip")
        _add_cache_estimate(actions, "pip", pip_cache)
    else:
        rc, out, err = run_command([sys.executable, "-m", "pip", "cache", "purge"], timeout=60)
        actions.append({"command": "pip cache purge", "rc": rc, "stdout": out[:200], "stderr": err[:200]})

    uv_cache = HOME / ".cache" / "uv"
    if uv_cache.exists():
        actions.append(safe_delete(uv_cache, dry_run))

    # HuggingFace cache is recyclable.
    if include_recyclable:
        hf_cache = HOME / ".cache" / "huggingface"
        if hf_cache.exists():
            actions.append(safe_delete(hf_cache, dry_run))

    # __pycache__ / .pytest_cache in project roots
    project_roots = [
        HOME / "projects",
        HOME / ".local",
        HOME / ".hyperai",
        HOME / ".codex",
        HOME / ".openclaw",
        ROOT,
    ]
    for root in project_roots:
        for found in find_matching_paths(root, {"__pycache__", ".pytest_cache"}):
            actions.append(safe_delete(found, dry_run))

    return actions


def recipe_npm(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []

    for tool, cmd, estimate_name in (
        ("npm", ["npm", "cache", "clean", "--force"], "npm"),
        ("pnpm", ["pnpm", "store", "prune"], "pnpm"),
        ("yarn", ["yarn", "cache", "clean"], "yarn"),
    ):
        executable = tool if tool != "pnpm" else "pnpm"
        if not shutil.which(executable):
            continue
        if dry_run:
            cache_dir = get_cache_dir(tool)
            _add_cache_estimate(actions, tool, cache_dir)
            if tool == "pnpm":
                # pnpm store prune removes unreferenced packages; estimate store size.
                store_path = get_cache_dir("pnpm")
                _add_cache_estimate(actions, "pnpm store prune (estimated)", store_path)
        else:
            rc, out, err = run_command(cmd, timeout=120)
            actions.append({"command": " ".join(cmd), "tool": tool, "rc": rc, "stdout": out[:200], "stderr": err[:200]})

    npm_cacache = HOME / ".npm" / "_cacache"
    if npm_cacache.exists():
        actions.append(safe_delete(npm_cacache, dry_run))

    if include_recyclable:
        # node_modules are recyclable; only remove under project roots where package.json exists.
        for root in (HOME / "projects", HOME / "HyperAI-Sync"):
            if not root.exists():
                continue
            for nm in root.rglob("node_modules"):
                if (nm.parent / "package.json").exists() or (nm.parent / "package-lock.json").exists():
                    actions.append(safe_delete(nm, dry_run))

    return actions


def recipe_homebrew(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    if not shutil.which("brew"):
        actions.append({"command": "brew", "status": "missing"})
        return actions

    if dry_run:
        rc, out, err = run_command(["brew", "cleanup", "-n", "-s"], timeout=120)
        actions.append({"command": "brew cleanup -n -s", "rc": rc, "stdout": out[:500], "stderr": err[:200], "status": "dry_run"})
    else:
        rc, out, err = run_command(["brew", "cleanup", "-s"], timeout=120)
        actions.append({"command": "brew cleanup -s", "rc": rc, "stdout": out[:500], "stderr": err[:200]})
    return actions


def recipe_vscode(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    for app_dir in (
        HOME / "Library" / "Application Support" / "Code",
        HOME / "Library" / "Application Support" / "Code - Insiders",
    ):
        if not app_dir.exists():
            continue
        for leaf in ("CachedExtensionVSIXs", "Crashpad", "logs"):
            target = app_dir / leaf
            actions.append(safe_delete(target, dry_run))

        if include_recyclable:
            for leaf in ("Cache", "CachedData", "CachedProfilesData"):
                target = app_dir / leaf
                actions.append(safe_delete(target, dry_run))

    return actions


def recipe_xcode(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []

    derived = HOME / "Library" / "Developer" / "Xcode" / "DerivedData"
    actions.append(safe_delete(derived, dry_run))

    if shutil.which("xcrun"):
        if dry_run:
            rc, out, err = run_command(["xcrun", "simctl", "list", "devices", "unavailable"], timeout=30)
            actions.append({"command": "xcrun simctl list devices unavailable", "rc": rc, "stdout": out[:200], "stderr": err[:200], "status": "dry_run"})
        else:
            rc, out, err = run_command(["xcrun", "simctl", "delete", "unavailable"], timeout=60)
            actions.append({"command": "xcrun simctl delete unavailable", "rc": rc, "stdout": out[:200], "stderr": err[:200]})

        if include_recyclable and not dry_run:
            rc2, out2, err2 = run_command(["xcrun", "simctl", "erase", "all"], timeout=120)
            actions.append({"command": "xcrun simctl erase all", "rc": rc2, "stdout": out2[:200], "stderr": err2[:200]})
        elif include_recyclable and dry_run:
            actions.append({"command": "xcrun simctl erase all", "status": "dry_run"})

    return actions


def recipe_docker(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    if not shutil.which("docker"):
        actions.append({"command": "docker", "status": "missing"})
        return actions

    rc, _, _ = run_command(["docker", "ps"], timeout=10)
    if rc != 0:
        actions.append({"command": "docker ps", "status": "daemon_unhealthy", "note": "skip docker prune"})
        return actions

    if dry_run:
        rc, out, err = run_command(["docker", "system", "df"], timeout=30)
        actions.append({"command": "docker system df", "rc": rc, "stdout": out[:500], "stderr": err[:200], "status": "dry_run"})
    else:
        for cmd in (["docker", "system", "prune", "-f"], ["docker", "builder", "prune", "-f"]):
            rc, out, err = run_command(cmd, timeout=120)
            actions.append({"command": " ".join(cmd), "rc": rc, "stdout": out[:500], "stderr": err[:200]})

    return actions


def recipe_ollama(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []

    cache = HOME / "Library" / "Caches" / "ollama"
    if cache.exists():
        actions.append(safe_delete(cache, dry_run))

    log_dir = HOME / ".ollama" / "logs"
    if log_dir.exists():
        now = time.time()
        for f in log_dir.glob("*.log"):
            if now - f.stat().st_mtime > 7 * 24 * 3600:
                actions.append(safe_delete(f, dry_run))

    if include_recyclable and shutil.which("ollama"):
        # List local models; removing unused models is gate-gated and not auto.
        rc, out, err = run_command(["ollama", "list"], timeout=30)
        actions.append({"command": "ollama list", "rc": rc, "stdout": out[:200], "stderr": err[:200], "status": "dry_run" if dry_run else "ok"})

    return actions


def recipe_macos(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    disposables = [
        HOME / "Library" / "Caches" / "pip",
        HOME / "Library" / "Caches" / "node-gyp",
        HOME / "Library" / "Caches" / "GeoServices",
        HOME / "Library" / "Caches" / "com.apple.helpd",
        HOME / "Library" / "Caches" / "com.apple.parsecd",
        HOME / "Library" / "Caches" / "typescript",
        HOME / "Library" / "Caches" / "fanal",
        HOME / "Library" / "Caches" / "com.grammarly.ProjectLlama",
        HOME / "Library" / "Caches" / "com.apple.python",
        HOME / "Library" / "Caches" / "com.openai.chat",
        HOME / ".cache" / "puppeteer",
        HOME / ".cache" / "clojure-lsp",
        HOME / ".cache" / "altimate-code",
        HOME / ".cache" / "opencode",
        HOME / ".cache" / "kilo",
        HOME / ".cache" / "chrome-devtools-mcp",
        HOME / ".cache" / "ms-playwright",
    ]
    for target in disposables:
        actions.append(safe_delete(target, dry_run))

    # Avoid Google cache while Chrome is running.
    chrome_running = False
    try:
        p = subprocess.run(["pgrep", "-x", "Google Chrome"], capture_output=True, text=True, timeout=5)
        chrome_running = p.returncode == 0
    except Exception:
        pass

    google_cache = HOME / "Library" / "Caches" / "Google"
    if google_cache.exists() and not chrome_running and include_recyclable:
        actions.append(safe_delete(google_cache, dry_run))

    return actions


def recipe_downloads(dry_run: bool, include_recyclable: bool) -> list[dict[str, Any]]:
    actions: list[dict[str, Any]] = []
    downloads = HOME / "Downloads"
    if not downloads.exists():
        return actions

    for pattern in ("*.crdownload", "*.part"):
        for f in downloads.glob(pattern):
            actions.append(safe_delete(f, dry_run))

    for f in downloads.rglob(".DS_Store"):
        actions.append(safe_delete(f, dry_run))

    if include_recyclable:
        now = time.time()
        for pattern in ("*.dmg", "*.pkg", "*.zip", "*.vsix"):
            for f in downloads.glob(pattern):
                if now - f.stat().st_mtime > 30 * 24 * 3600:
                    actions.append(safe_delete(f, dry_run))

    return actions


RECIPES = {
    "pip": recipe_pip,
    "npm": recipe_npm,
    "homebrew": recipe_homebrew,
    "vscode": recipe_vscode,
    "xcode": recipe_xcode,
    "docker": recipe_docker,
    "ollama": recipe_ollama,
    "macos": recipe_macos,
    "downloads": recipe_downloads,
}


def estimate_freed_mb(actions: list[dict[str, Any]]) -> float:
    total = 0.0
    for a in actions:
        if a.get("status") in ("deleted", "dry_run"):
            total += a.get("estimated_mb", 0.0)
        if "stdout" in a and "MB" in a.get("stdout", ""):
            # rough heuristic for pip cache purge output
            m = re.search(r"([0-9.]+)\s*MB", a["stdout"])
            if m:
                total += float(m.group(1))
    return round(total, 2)


def execute_system(
    system: str,
    dry_run: bool,
    include_recyclable: bool,
) -> dict[str, Any]:
    if system not in RECIPES:
        return {"system": system, "status": "unknown", "actions": []}

    disk_before = disk_free_mb()
    started_at = now_iso()
    actions = RECIPES[system](dry_run, include_recyclable)
    disk_after = disk_free_mb()

    freed_mb = max(0, disk_after - disk_before) if not dry_run else estimate_freed_mb(actions)
    errors = [a for a in actions if a.get("status") == "error"]

    result = {
        "schema_version": "2026-07-27.cleanup-receipt.v1",
        "system": system,
        "started_at": started_at,
        "completed_at": now_iso(),
        "dry_run": dry_run,
        "include_recyclable": include_recyclable,
        "disk_before_mb": disk_before,
        "disk_after_mb": disk_after,
        "freed_mb": freed_mb,
        "action_count": len(actions),
        "error_count": len(errors),
        "actions": actions,
        "status": "ok" if not errors else "partial",
    }
    return result


def write_receipt(result: dict[str, Any]) -> Path:
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    safe_name = re.sub(r"[^a-z0-9_-]", "_", result["system"].lower())
    path = RECEIPT_DIR / f"{ts}_{safe_name}.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HyperAI system cleanup executor")
    parser.add_argument(
        "--systems",
        default="auto",
        help="Comma-separated systems or 'all'/'auto'",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without mutating")
    parser.add_argument("--approve-recycle", action="store_true", help="Include recyclable-class actions")
    parser.add_argument("--proof-dir", default=str(RECEIPT_DIR), help="Receipt output directory")
    return parser.parse_args()


def select_systems(systems_arg: str, free_mb: int, approve_recycle: bool) -> tuple[list[str], bool]:
    include_recyclable = approve_recycle or free_mb < 2048

    if systems_arg == "all":
        return list(RECIPES.keys()), include_recyclable
    if systems_arg == "auto":
        if free_mb < 0:
            return list(RECIPES.keys()), include_recyclable
        if free_mb < 2048:
            return list(RECIPES.keys()), True
        if free_mb < 10240:
            return list(RECIPES.keys()), False
        return [], False
    return [s.strip() for s in systems_arg.split(",")], include_recyclable


def main() -> int:
    args = parse_args()
    free_mb = disk_free_mb()
    systems, include_recyclable = select_systems(args.systems, free_mb, args.approve_recycle)

    if not systems:
        print(json.dumps({"status": "skipped", "reason": "disk_stable", "free_mb": free_mb}, indent=2))
        return 0

    print(
        f"Cleanup executor: free_mb={free_mb}, systems={systems}, dry_run={args.dry_run}, "
        f"include_recyclable={include_recyclable}",
        file=sys.stderr,
    )

    all_results: list[dict[str, Any]] = []
    for system in systems:
        print(f"  -> running {system} ...", file=sys.stderr)
        result = execute_system(system, args.dry_run, include_recyclable)
        receipt_path = write_receipt(result)
        result["receipt_path"] = str(receipt_path)
        all_results.append(result)
        print(f"     {result['status']} freed={result['freed_mb']}MB errors={result['error_count']}", file=sys.stderr)

    summary = {
        "status": "ok" if all(r["status"] == "ok" for r in all_results) else "partial",
        "free_mb_before": free_mb,
        "free_mb_after": disk_free_mb(),
        "systems_run": systems,
        "dry_run": args.dry_run,
        "include_recyclable": include_recyclable,
        "receipts": [r["receipt_path"] for r in all_results],
        "details": all_results,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())