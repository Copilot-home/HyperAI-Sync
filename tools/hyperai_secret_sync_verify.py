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
"""Verify SecretStorage sync reality across all anchored surfaces.

Tests:
- .canon_env and .apo_secret_sync symlinks on every target surface
- env var propagation (file + launchctl)
- Python ↔ TypeScript round-trip through the canonical vault
- APO bundle coherence (SECRETS_SYNC, APO_cleanup)
- brain.index audit trail
"""

import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path("/Users/andy")
GLOBAL_ENV = HOME / ".config" / "axcanon" / "global.env"
SECRETS_DIR = HOME / ".axcanon" / "memory" / "secrets"
PY_TOOL = HOME / "HyperAI-Sync" / "tools" / "hyperai_vscode_secret_sync.py"
TS_DIST = HOME / "HyperAI-Sync" / "vscode-secret-sync" / "dist" / "index.js"

TARGET_CATEGORIES = {
    "dev_tool",
    "ai_operator_runtime",
    "ai_canon_identity_memory",
    "ai_forensic_evidence",
    "ai_project_lab",
    "gke_lab",
    "daiof_sandbox",
    "vscode_extension",
    "generic_project",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_catalog_records() -> list[dict]:
    catalog_dir = HOME / ".axcanon" / "memory" / "home_catalog"
    bundle_files = sorted(catalog_dir.glob("*_HOME_CATALOG_bundle.json"))
    if not bundle_files:
        raise FileNotFoundError("No HOME_CATALOG bundle")
    return json.loads(bundle_files[-1].read_text()).get("records", [])


def verify_surface_links(rec: dict) -> dict:
    path = Path(rec["path"])
    res = {
        "path": str(path),
        "category": rec.get("category"),
        "exists": path.exists(),
        "canon_env_exists": False,
        "canon_env_target_ok": False,
        "apo_secret_sync_exists": False,
        "apo_secret_sync_target_ok": False,
        "error": None,
    }
    if not path.is_dir():
        res["error"] = "not a directory"
        return res

    def check(link: Path, expected: Path) -> tuple[bool, bool]:
        exists = link.is_symlink() or link.exists()
        target_ok = link.is_symlink() and os.path.exists(link) and os.readlink(link) == str(expected)
        return exists, target_ok

    res["canon_env_exists"], res["canon_env_target_ok"] = check(
        path / ".canon_env", GLOBAL_ENV
    )
    res["apo_secret_sync_exists"], res["apo_secret_sync_target_ok"] = check(
        path / ".apo_secret_sync", SECRETS_DIR / "SECRETS_SYNC_INDEX.json"
    )
    return res


def verify_env_file() -> dict:
    res = {"exists": GLOBAL_ENV.exists(), "keys": {}}
    if not GLOBAL_ENV.exists():
        return res
    text = GLOBAL_ENV.read_text()
    required = [
        "AX_APO_SECRET_LIBRARY",
        "AX_SECRET_VAULT_PATH",
        "AX_SECRET_VAULT_SERVICE",
        "AX_SECRET_VAULT_ACCOUNT",
        "AX_SECRET_SYNC_INDEX",
        "AX_SECRET_KEY_FILE",
        "AX_SECRET_TS_MODULE",
        "AX_SECRET_PY_TOOL",
    ]
    for k in required:
        m = re.search(rf'export\s+{k}\s*=\s*"([^"]+)"', text)
        res["keys"][k] = m.group(1) if m else None
    res["all_present"] = all(v is not None for v in res["keys"].values())
    return res


def verify_launchctl_env() -> dict:
    res = {}
    for k in ["AX_SECRET_SYNC_INDEX", "AX_SECRET_VAULT_PATH", "AX_APO_SECRET_LIBRARY"]:
        try:
            out = subprocess.run(["launchctl", "getenv", k], capture_output=True, text=True, check=False)
            res[k] = out.stdout.strip() or None
        except FileNotFoundError:
            res[k] = None
    res["ok"] = all(res.values())
    return res


def python_round_trip() -> dict:
    res = {"set_ok": False, "get_ok": False, "value": None, "error": None}
    test_key = f"apo.verify.{os.getpid()}"
    test_val = f"verified-{now_iso()}"
    try:
        s = subprocess.run(
            [sys.executable, str(PY_TOOL), "set", test_key, test_val],
            capture_output=True,
            text=True,
            check=False,
        )
        res["set_ok"] = s.returncode == 0
        if not res["set_ok"]:
            res["error"] = s.stderr.strip()
            return res
        g = subprocess.run(
            [sys.executable, str(PY_TOOL), "get", test_key],
            capture_output=True,
            text=True,
            check=False,
        )
        res["get_ok"] = g.returncode == 0 and g.stdout.strip() == test_val
        res["value"] = g.stdout.strip() if g.returncode == 0 else None
        # cleanup
        subprocess.run([sys.executable, str(PY_TOOL), "delete", test_key], capture_output=True, check=False)
    except Exception as e:
        res["error"] = str(e)
    return res


def ts_round_trip() -> dict:
    res = {"set_ok": False, "get_ok": False, "value": None, "error": None}
    if not TS_DIST.exists():
        res["error"] = f"TS module not built: {TS_DIST}"
        return res
    test_key = f"apo.ts.verify.{os.getpid()}"
    test_val = f"ts-verified-{now_iso()}"
    env = os.environ.copy()
    env["AX_SECRET_KEY_FILE"] = str(SECRETS_DIR / "master.key")
    script = f"""
const {{ APOSecretStorageSync }} = require('{TS_DIST}');
(async () => {{
  const s = await APOSecretStorageSync.create();
  await s.store('{test_key}', '{test_val}');
  const v = await s.get('{test_key}');
  await s.delete('{test_key}');
  console.log(v);
}})();
"""
    try:
        out = subprocess.run(["node", "-e", script], capture_output=True, text=True, env=env, check=False)
        res["value"] = out.stdout.strip() if out.returncode == 0 else None
        res["set_ok"] = out.returncode == 0
        res["get_ok"] = out.returncode == 0 and out.stdout.strip() == test_val
        if not res["get_ok"]:
            res["error"] = out.stderr.strip() or "TS round-trip mismatch"
    except Exception as e:
        res["error"] = str(e)
    return res


def python_ts_cross_sync() -> dict:
    res = {"py_set_ok": False, "ts_get_ok": False, "value": None, "error": None}
    test_key = f"apo.cross.{os.getpid()}"
    test_val = f"cross-{now_iso()}"
    try:
        s = subprocess.run(
            [sys.executable, str(PY_TOOL), "set", test_key, test_val],
            capture_output=True,
            text=True,
            check=False,
        )
        res["py_set_ok"] = s.returncode == 0
        if not res["py_set_ok"]:
            res["error"] = s.stderr.strip()
            return res

        env = os.environ.copy()
        env["AX_SECRET_KEY_FILE"] = str(SECRETS_DIR / "master.key")
        script = f"""
const {{ APOSecretStorageSync }} = require('{TS_DIST}');
(async () => {{
  const s = await APOSecretStorageSync.create();
  const v = await s.get('{test_key}');
  await s.delete('{test_key}');
  console.log(v);
}})();
"""
        out = subprocess.run(["node", "-e", script], capture_output=True, text=True, env=env, check=False)
        res["value"] = out.stdout.strip() if out.returncode == 0 else None
        res["ts_get_ok"] = out.returncode == 0 and out.stdout.strip() == test_val
        if not res["ts_get_ok"]:
            res["error"] = out.stderr.strip() or "cross-sync mismatch"
    except Exception as e:
        res["error"] = str(e)
    return res


def read_brain_index() -> dict:
    path = HOME / ".axcanon" / "memory" / "brain.index"
    if not path.exists():
        return {"exists": False, "lines": 0, "last": None}
    lines = path.read_text().strip().splitlines()
    return {"exists": True, "lines": len(lines), "last": lines[-1] if lines else None}


def read_apo_index() -> dict:
    path = HOME / "HyperAI-Sync" / "runtime" / "federation_orchestrator" / "cleanup_receipts" / "APO_cleanup_index.json"
    if not path.exists():
        return {"exists": False}
    return json.loads(path.read_text())


def read_secrets_index() -> dict:
    path = SECRETS_DIR / "SECRETS_SYNC_INDEX.json"
    if not path.exists():
        return {"exists": False}
    return json.loads(path.read_text())


def main():
    print(f"=== SecretStorage sync verification started at {now_iso()} ===")

    records = load_catalog_records()
    target_records = [r for r in records if r.get("category") in TARGET_CATEGORIES]

    print(f"[catalog] {len(target_records)} target surfaces")

    surface_results = [verify_surface_links(r) for r in target_records]
    ok_surfaces = [s for s in surface_results if s["canon_env_target_ok"] and s["apo_secret_sync_target_ok"]]
    bad_surfaces = [s for s in surface_results if s not in ok_surfaces]

    env_file = verify_env_file()
    launchctl = verify_launchctl_env()
    py_test = python_round_trip()
    ts_test = ts_round_trip()
    cross_test = python_ts_cross_sync()
    brain = read_brain_index()
    apo_index = read_apo_index()
    secrets_index = read_secrets_index()

    print(f"[anchors] {len(ok_surfaces)}/{len(surface_results)} surfaces fully anchored")
    if bad_surfaces:
        print(f"[drift ] {len(bad_surfaces)} surfaces need repair")
        for s in bad_surfaces[:10]:
            print(f"  - {s['path']}: env={s['canon_env_target_ok']} sync={s['apo_secret_sync_target_ok']} err={s.get('error')}")

    print(f"[env file] {env_file.get('all_present', False)} ({len(env_file['keys'])} keys)")
    print(f"[launchctl] {launchctl.get('ok', False)}")
    print(f"[python  ] set={py_test['set_ok']} get={py_test['get_ok']}")
    print(f"[typescript] set={ts_test['set_ok']} get={ts_test['get_ok']}")
    print(f"[cross-sync] py_set={cross_test['py_set_ok']} ts_get={cross_test['ts_get_ok']}")
    print(f"[brain   ] {brain['lines']} lines, last: {brain['last']}")
    print(f"[apo     ] {apo_index.get('artifact_count', 0)} artifacts, Ω={apo_index.get('global_omega')}")
    print(f"[secrets ] {secrets_index.get('artifact_count', 0)} surfaces, Ω={secrets_index.get('global_omega')}")

    report = {
        "schema_version": "SECRET_SYNC_VERIFY_V1",
        "verified_at": now_iso(),
        "surfaces": {
            "total": len(surface_results),
            "ok": len(ok_surfaces),
            "bad": len(bad_surfaces),
        },
        "env_file": env_file,
        "launchctl": launchctl,
        "python_test": py_test,
        "typescript_test": ts_test,
        "cross_sync_test": cross_test,
        "brain_index": brain,
        "apo_index": apo_index,
        "secrets_index": secrets_index,
        "drift": bad_surfaces[:20],
    }

    report_path = SECRETS_DIR / "SECRETS_SYNC_VERIFY.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False))
    print(f"[report  ] {report_path}")

    all_ok = (
        len(bad_surfaces) == 0
        and env_file.get("all_present")
        and launchctl.get("ok")
        and py_test["get_ok"]
        and ts_test["get_ok"]
        and cross_test["ts_get_ok"]
    )
    print(f"[verdict ] {'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
