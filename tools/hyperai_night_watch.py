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
"""Σ_APΩ night-watch / sleep workflow for HyperAI-Sync.

When the creator is asleep or idle, this patrol keeps the runtime honest:
- probes canonical ports and disk
- verifies Σ_APΩ canon anchors across all surfaces
- verifies SecretStorage sync
- re-bakes APO bundle if drift is detected
- dry-runs AIOS cleanup to estimate risk
- writes an alert if Ω drops or disk becomes critical

No destructive action is taken without an explicit gate. PR triage and cloud
mutation are intentionally excluded from the default patrol.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, "/Users/andy/HyperAI-Sync/tools")
import hyperai_runtime_policy as runtime_policy


HOME = Path("/Users/andy")
ROOT = HOME / "HyperAI-Sync"
MEMORY = HOME / ".axcanon" / "memory"
SLEEP_FLAG = MEMORY / "sleep_mode.json"
LOG_PATH = MEMORY / "night_watch_log.jsonl"
SUMMARY_PATH = MEMORY / "night_watch_summary.json"
ALERT_PATH = MEMORY / "night_watch_alert.json"
PLIST_PATH = HOME / "Library" / "LaunchAgents" / "com.hyperai.nightwatch.plist"

PATROL_INTERVAL_SECONDS = 30 * 60


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def log_event(event: dict[str, Any]) -> None:
    MEMORY.mkdir(parents=True, mode=0o700, exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def run_command(cmd: list[str], timeout: int = 300) -> tuple[int, str, str]:
    env = os.environ.copy()
    # Ensure canon env is visible to child scripts.
    global_env = HOME / ".config" / "axcanon" / "global.env"
    if global_env.exists():
        for line in global_env.read_text().splitlines():
            if line.startswith("export "):
                kv = line[7:].strip().split("=", 1)
                if len(kv) == 2:
                    env[kv[0]] = kv[1].strip('"')
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as e:
        return -9, "", f"timeout after {timeout}s: {e}"
    except Exception as e:
        return -1, "", f"exception: {e}"


def parse_sleep_hours() -> tuple[int, int] | None:
    raw = os.environ.get("HYPERAI_SLEEP_HOURS", "")
    if not raw:
        return None
    try:
        start, end = raw.split("-")
        return int(start), int(end)
    except Exception:
        return None


def is_sleep() -> bool:
    if SLEEP_FLAG.exists():
        try:
            flag = json.loads(SLEEP_FLAG.read_text())
            if flag.get("sleep") is True:
                return True
        except Exception:
            pass
    hours = parse_sleep_hours()
    if hours:
        now_hour = datetime.now().hour
        start, end = hours
        if start <= end:
            return start <= now_hour < end
        return now_hour >= start or now_hour < end
    return False


def set_sleep(sleep: bool) -> None:
    MEMORY.mkdir(parents=True, mode=0o700, exist_ok=True)
    if sleep:
        SLEEP_FLAG.write_text(json.dumps({"sleep": True, "since": now_iso(), "toggled_by": "manual"}, indent=2))
    else:
        if SLEEP_FLAG.exists():
            SLEEP_FLAG.unlink()


def probe_runtime() -> dict[str, Any]:
    policy = runtime_policy.build_policy_snapshot()
    return {
        "disk_free_mb": policy.get("disk_free_mb"),
        "disk_state": policy.get("disk_state"),
        "backend_classification": policy.get("backend_classification"),
        "frontend_classification": policy.get("frontend_classification"),
        "core_ready": policy.get("core_ready"),
        "operator_attention_required": policy.get("operator_attention_required"),
        "action_reason": policy.get("action_reason"),
    }


def run_sigma_verify() -> dict[str, Any]:
    rc, out, err = run_command([sys.executable, "tools/hyperai_sigma_apo_verify.py"], timeout=600)
    return {"script": "sigma_apo_verify", "rc": rc, "ok": rc == 0, "stdout_tail": out[-800:], "stderr_tail": err[-400:]}


def run_secret_verify() -> dict[str, Any]:
    rc, out, err = run_command([sys.executable, "tools/hyperai_secret_sync_verify.py"], timeout=600)
    return {"script": "secret_sync_verify", "rc": rc, "ok": rc == 0, "stdout_tail": out[-800:], "stderr_tail": err[-400:]}


def run_cleanup_dryrun() -> dict[str, Any]:
    rc, out, err = run_command([sys.executable, "tools/hyperai_cleanup_executor.py", "--dry-run"], timeout=600)
    return {"script": "cleanup_executor", "rc": rc, "ok": rc == 0, "stdout_tail": out[-1000:], "stderr_tail": err[-400:]}


def run_apo_standardize() -> dict[str, Any]:
    rc, out, err = run_command([sys.executable, "tools/hyperai_canon_standardize.py"], timeout=600)
    return {"script": "canon_standardize", "rc": rc, "ok": rc == 0, "stdout_tail": out[-1000:], "stderr_tail": err[-400:]}


def run_notebooklm_compile() -> dict[str, Any]:
    cmd = [sys.executable, "tools/hyperai_notebooklm_compile.py"]
    if os.environ.get("AX_NOTEBOOKLM_DRIVE_ENABLED"):
        cmd.append("--drive-sync")
    if os.environ.get("AX_NOTEBOOKLM_CONSUMER_ENABLED"):
        cmd.append("--consumer-sync")
    rc, out, err = run_command(cmd, timeout=900)
    return {"script": "notebooklm_compile", "rc": rc, "ok": rc == 0, "stdout_tail": out[-500:], "stderr_tail": err[-400:]}


def build_alert(summary: dict[str, Any]) -> dict[str, Any] | None:
    alerts: list[str] = []
    runtime = summary.get("runtime_probe", {})
    if runtime.get("disk_state") == "CRITICAL":
        alerts.append(f"Disk critical: {runtime.get('disk_free_mb')} MiB free")
    if runtime.get("disk_state") == "MINIMUM_RECOVERED":
        alerts.append(f"Disk low: {runtime.get('disk_free_mb')} MiB free")
    checks = summary.get("checks", {})
    if not checks.get("sigma_verify", {}).get("ok"):
        alerts.append("Σ_APΩ surface verify failed")
    if not checks.get("secret_verify", {}).get("ok"):
        alerts.append("SecretStorage sync verify failed")
    if not checks.get("apo_standardize", {}).get("ok"):
        alerts.append("APO re-bake failed")
    if not checks.get("notebooklm_compile", {}).get("ok"):
        alerts.append("NotebookLM compile failed")
    omega = summary.get("omega", 1)
    if omega < 1:
        alerts.append(f"Ω = {omega} (< 1)")
    if not alerts:
        return None
    return {
        "at": now_iso(),
        "alerts": alerts,
        "summary": summary,
    }


def send_notification(title: str, message: str) -> None:
    if platform.system() != "Darwin":
        return
    try:
        subprocess.run(
            ["osascript", "-e", f'display notification "{message}" with title "{title}"'],
            capture_output=True,
            timeout=10,
            check=False,
        )
    except Exception:
        pass


def patrol(force: bool = False) -> dict[str, Any]:
    asleep = is_sleep() or force
    status = {
        "at": now_iso(),
        "asleep": asleep,
        "forced": force,
        "runtime_probe": {},
        "checks": {},
        "omega": 1,
        "alert": None,
    }
    if not asleep:
        status["note"] = "Creator awake; no patrol executed."
        log_event(status)
        SUMMARY_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False))
        return status

    status["runtime_probe"] = probe_runtime()
    status["checks"]["sigma_verify"] = run_sigma_verify()
    status["checks"]["secret_verify"] = run_secret_verify()
    status["checks"]["apo_standardize"] = run_apo_standardize()
    status["checks"]["notebooklm_compile"] = run_notebooklm_compile()
    status["checks"]["cleanup_dryrun"] = run_cleanup_dryrun()

    omega = 1
    if not status["checks"]["sigma_verify"]["ok"]:
        omega = 0
    if not status["checks"]["secret_verify"]["ok"]:
        omega = 0
    if not status["checks"]["apo_standardize"]["ok"]:
        omega = 0
    if not status["checks"]["notebooklm_compile"]["ok"]:
        omega = 0
    if status["runtime_probe"].get("disk_state") == "CRITICAL":
        omega = 0
    status["omega"] = omega

    alert = build_alert(status)
    if alert:
        status["alert"] = alert
        ALERT_PATH.write_text(json.dumps(alert, indent=2, ensure_ascii=False))
        send_notification("HyperAI Night Watch", "; ".join(alert["alerts"]))
    else:
        if ALERT_PATH.exists():
            ALERT_PATH.unlink()

    log_event(status)
    SUMMARY_PATH.write_text(json.dumps(status, indent=2, ensure_ascii=False))
    return status


def install_launchd() -> dict[str, Any]:
    PLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    plist = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.hyperai.nightwatch</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{ROOT / "tools" / "hyperai_night_watch.py"}</string>
        <string>--run</string>
    </array>
    <key>StartInterval</key>
    <integer>{PATROL_INTERVAL_SECONDS}</integer>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>{MEMORY / "night_watch_stdout.log"}</string>
    <key>StandardErrorPath</key>
    <string>{MEMORY / "night_watch_stderr.log"}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>HYPERAI_SLEEP_HOURS</key>
        <string>{os.environ.get("HYPERAI_SLEEP_HOURS", "")}</string>
        <key>AX_NOTEBOOKLM_DRIVE_ENABLED</key>
        <string>{os.environ.get("AX_NOTEBOOKLM_DRIVE_ENABLED", "")}</string>
    </dict>
</dict>
</plist>
"""
    PLIST_PATH.write_text(plist)
    rc, out, err = run_command(["launchctl", "load", str(PLIST_PATH)])
    return {"installed": True, "plist": str(PLIST_PATH), "rc": rc, "stdout": out, "stderr": err}


def uninstall_launchd() -> dict[str, Any]:
    rc = 0
    if PLIST_PATH.exists():
        rc, out, err = run_command(["launchctl", "unload", str(PLIST_PATH)])
        try:
            PLIST_PATH.unlink()
        except Exception as e:
            return {"uninstalled": False, "error": str(e)}
    return {"uninstalled": True, "rc": rc}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Σ_APΩ night watch / sleep workflow")
    parser.add_argument("--run", action="store_true", help="Execute one patrol cycle if asleep")
    parser.add_argument("--force", action="store_true", help="Run patrol even if not in sleep mode (test)")
    parser.add_argument("--toggle-sleep", action="store_true", help="Toggle sleep mode on/off")
    parser.add_argument("--status", action="store_true", help="Print current sleep and last summary")
    parser.add_argument("--install", action="store_true", help="Install launchd agent")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall launchd agent")
    parser.add_argument("--interval", type=int, default=PATROL_INTERVAL_SECONDS, help="Patrol interval in seconds")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.toggle_sleep:
        new_state = not is_sleep()
        set_sleep(new_state)
        print(json.dumps({"sleep_mode": new_state, "flag": str(SLEEP_FLAG), "at": now_iso()}, indent=2))
        return 0
    if args.status:
        last = {}
        if SUMMARY_PATH.exists():
            try:
                last = json.loads(SUMMARY_PATH.read_text())
            except Exception:
                pass
        print(json.dumps({"sleep": is_sleep(), "flag": str(SLEEP_FLAG), "last_summary": last}, indent=2))
        return 0
    if args.install:
        if args.interval:
            global PATROL_INTERVAL_SECONDS
            PATROL_INTERVAL_SECONDS = args.interval
        result = install_launchd()
        print(json.dumps(result, indent=2))
        return 0 if result.get("installed") else 1
    if args.uninstall:
        print(json.dumps(uninstall_launchd(), indent=2))
        return 0

    summary = patrol(force=args.force)
    print(json.dumps(summary, indent=2))
    return 0 if summary.get("omega", 0) == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
