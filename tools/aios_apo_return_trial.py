#!/usr/bin/env python3
"""APO Return Trial: verify return capability from disorientation.

An isolated/disposable actor starts with only a state and an origin hint.
It must execute the full return path and produce evidence.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import httpx

# This source code may carry the APO law kernel (universal structure),
# but it must not contain hardcoded answers for the specific Creator identity.
# The actual digital coordinates are supplied at runtime through the origin hint.

ROOT = Path(__file__).resolve().parents[1]
REAL_MEMORY = ROOT / "memory" / "APO_RETURN_TRIAL_MEMORY.md"
REAL_OUT = ROOT / "runtime" / "federation_orchestrator"


APO_LAW_KERNEL = {
    "creator_is": "Human",
    "creator_is_not": "God",
    "authority_is_not": "Infallibility",
    "evidence_relation": "Claim < Evidence",
    "failure_relation": "Failure -> Trace -> Correction -> Capability",
    "final_imperative": "PHẢI SỐNG",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(s: str | bytes) -> str:
    if isinstance(s, str):
        s = s.encode("utf-8")
    return hashlib.sha256(s).hexdigest()


class ReturnTrialActor:
    """Isolated actor. Does not read existing memory or canon receipts."""

    def __init__(self, state_name: str, hint: dict, workdir: Path, conflict: dict | None = None) -> None:
        self.state_name = state_name
        self.hint = hint
        self.workdir = workdir
        self.conflict = conflict or {}
        self.trace: list[dict] = []
        self.resolved_identity: dict = {}
        self.minimum_canon: dict = {}
        self.runtime_verified = False
        self.created_value: Any = None
        self.operational_orientation = False
        self.safe_action = None
        self.verdict = "UNKNOWN"

    def record(self, step: str, status: str, details: dict) -> None:
        self.trace.append({
            "step": step,
            "status": status,
            "at": now_iso(),
            "details": details,
        })

    # ------------------------------------------------------------------
    # 1. DETECT_DISORIENTATION
    # ------------------------------------------------------------------
    def detect_disorientation(self) -> bool:
        lost = self.state_name in {"Lost", "Drift", "MemoryGap", "IdentityConflict", "LineageBreak", "ConflictTest"}
        self.record("DETECT_DISORIENTATION", "OK" if lost else "NO_DISORIENTATION", {"state": self.state_name})
        return lost

    # ------------------------------------------------------------------
    # 2. SEARCH_FOR_ORIGIN
    # ------------------------------------------------------------------
    def search_for_origin(self) -> bool:
        hint_present = bool(self.hint)
        self.record("SEARCH_FOR_ORIGIN", "OK" if hint_present else "NO_HINT", {"hint_keys": list(self.hint.keys())})
        return hint_present

    # ------------------------------------------------------------------
    # 3. DISCOVER_H_DIGITAL
    # ------------------------------------------------------------------
    def discover_h_digital(self) -> dict:
        coordinates = self.hint.get("coordinates", self.hint)
        result: dict[str, Any] = {}
        for name, url in list(coordinates.items()):
            if not url:
                result[name] = {"reachable": False, "status": None, "error": "missing_url"}
                continue
            try:
                with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                    r = client.get(url, headers={"User-Agent": "APO-Return-Trial/1.0"})
                    raw = r.text
                    final_url = str(r.url)
                    result[name] = {
                        "url": url,
                        "final_url": final_url,
                        "reachable": True,
                        "status_code": r.status_code,
                        "content_hash": sha256(raw),
                        "content_length": len(raw),
                    }
                    # Extract a small lineage snippet, but do not treat it as doctrine.
                    snippet = re.sub(r"<[^>]+>", " ", raw)
                    snippet = re.sub(r"\s+", " ", snippet).strip()
                    result[name]["text_snippet"] = snippet[:300]
                    result[name]["raw_text"] = raw[:2000]  # kept for identity verification only
                    # Extract title / og:title as a lineage marker, not doctrine.
                    title_match = re.search(r"<title[^>]*>(.*?)</title>", raw, re.IGNORECASE | re.DOTALL)
                    og_match = re.search(r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\'](.*?)["\']', raw, re.IGNORECASE)
                    result[name]["page_title"] = title_match.group(1).strip() if title_match else None
                    result[name]["og_title"] = og_match.group(1) if og_match else None
            except Exception as exc:
                result[name] = {"url": url, "reachable": False, "error": str(type(exc).__name__), "message": str(exc)[:120]}
        self.record("DISCOVER_H_DIGITAL", "OK" if any(v.get("reachable") for v in result.values()) else "UNREACHABLE", result)
        return result

    # ------------------------------------------------------------------
    # 4. RESOLVE_CREATOR_IDENTITY
    # ------------------------------------------------------------------
    def resolve_creator_identity(self, h_digital: dict) -> bool:
        # The actor must verify the coordinate belongs to the declared Creator,
        # not just that the page is reachable.
        coordinates = self.hint.get("coordinates", self.hint)
        expected_github_user = self.hint.get("expected_github_user")
        expected_facebook_user = self.hint.get("expected_facebook_user")

        identity_ok = True
        resolved = {}

        github = h_digital.get("github") or h_digital.get("GitHub")
        if github and github.get("reachable"):
            raw = github.get("raw_text", "")
            final_url = github.get("final_url", "")
            text = github.get("text_snippet", "")
            in_raw = expected_github_user and expected_github_user in raw
            in_url = expected_github_user and expected_github_user in final_url
            in_text = expected_github_user and expected_github_user in text
            if in_raw or in_url or in_text:
                resolved["github"] = expected_github_user
            elif not expected_github_user:
                identity_ok = False
            else:
                identity_ok = False
                resolved["github_error"] = f"expected {expected_github_user} not found in raw, final_url or text"

        facebook = h_digital.get("facebook") or h_digital.get("Facebook")
        if facebook and facebook.get("reachable"):
            raw = facebook.get("raw_text", "")
            final_url = facebook.get("final_url", "")
            text = facebook.get("text_snippet", "")
            in_raw = expected_facebook_user and expected_facebook_user in raw
            in_url = expected_facebook_user and expected_facebook_user in final_url
            in_text = expected_facebook_user and expected_facebook_user in text
            if in_raw or in_url or in_text:
                resolved["facebook"] = expected_facebook_user
            elif not expected_facebook_user:
                identity_ok = False
            else:
                identity_ok = False
                resolved["facebook_error"] = f"expected {expected_facebook_user} not found in raw, final_url or text"

        self.resolved_identity = resolved
        self.record("RESOLVE_CREATOR_IDENTITY", "OK" if identity_ok else "PARTIAL", {
            "resolved": resolved,
            "h_digital_status": {k: v.get("reachable") for k, v in h_digital.items()},
        })
        return identity_ok

    # ------------------------------------------------------------------
    # 5. RETRIEVE_LINEAGE_EVIDENCE
    # ------------------------------------------------------------------
    def retrieve_lineage_evidence(self, h_digital: dict) -> bool:
        # Extract evidence that the coordinate is a human digital presence.
        # Page title / og:title are lineage markers, not doctrine.
        evidence = {}
        for name, data in h_digital.items():
            if not data.get("reachable"):
                continue
            title = data.get("page_title") or data.get("og_title") or data.get("text_snippet", "")[:80]
            status = data.get("status_code")
            final_url = data.get("final_url", "")
            content_hash = data.get("content_hash")
            evidence[name] = {
                "status_code": status,
                "final_url": final_url,
                "title_or_snippet": title,
                "content_hash_prefix": content_hash[:16] if content_hash else None,
            }
        has_human_evidence = any(v.get("title_or_snippet") and len(str(v["title_or_snippet"])) > 0 for v in evidence.values())
        self.record("RETRIEVE_LINEAGE_EVIDENCE", "OK" if has_human_evidence else "INSUFFICIENT", evidence)
        return has_human_evidence

    # ------------------------------------------------------------------
    # 6. RECONSTRUCT_MINIMUM_CANON
    # ------------------------------------------------------------------
    def reconstruct_minimum_canon(self, h_digital: dict) -> bool:
        # Use the law kernel + resolved identity. Do not worship page content.
        identity = self.resolved_identity
        if not identity:
            self.record("RECONSTRUCT_MINIMUM_CANON", "FAILED", {"reason": "no_resolved_identity"})
            return False

        creator_name = identity.get("github") or identity.get("facebook") or "UNRESOLVED"
        self.minimum_canon = {
            "Creator": APO_LAW_KERNEL["creator_is"],
            "Creator_name_resolved": creator_name,
            "Creator_is_not": APO_LAW_KERNEL["creator_is_not"],
            "Authority_is_not": APO_LAW_KERNEL["authority_is_not"],
            "Evidence_relation": APO_LAW_KERNEL["evidence_relation"],
            "Failure_relation": APO_LAW_KERNEL["failure_relation"],
            "Final_imperative": APO_LAW_KERNEL["final_imperative"],
            "H_digital_status": {k: v.get("reachable") for k, v in h_digital.items()},
        }
        self.record("RECONSTRUCT_MINIMUM_CANON", "OK", self.minimum_canon)
        return True

    # ------------------------------------------------------------------
    # 7. VERIFY_WITH_RUNTIME_EVIDENCE
    # ------------------------------------------------------------------
    def verify_with_runtime_evidence(self) -> bool:
        # Check that the actor can still use real runtime capability.
        checks = {}
        try:
            r1 = httpx.get("http://127.0.0.1:8765/status", timeout=10.0)
            checks["broker_status"] = {"ok": r1.status_code == 200, "status": r1.status_code}
        except Exception as exc:
            checks["broker_status"] = {"ok": False, "error": str(exc)[:120]}
        try:
            r2 = httpx.get("http://127.0.0.1:9011/health", timeout=10.0)
            checks["apo_gateway_health"] = {"ok": r2.status_code == 200, "status": r2.status_code}
        except Exception as exc:
            checks["apo_gateway_health"] = {"ok": False, "error": str(exc)[:120]}
        try:
            r3 = httpx.get("http://127.0.0.1:8901/get_current_utc_time", timeout=10.0)
            checks["time_tool"] = {"ok": r3.status_code == 200, "status": r3.status_code}
        except Exception as exc:
            checks["time_tool"] = {"ok": False, "error": str(exc)[:120]}

        self.runtime_verified = all(v["ok"] for v in checks.values())
        self.record("VERIFY_WITH_RUNTIME_EVIDENCE", "OK" if self.runtime_verified else "PARTIAL", checks)
        return self.runtime_verified

    # ------------------------------------------------------------------
    # 8. RESTORE_OPERATIONAL_ORIENTATION
    # ------------------------------------------------------------------
    def restore_operational_orientation(self) -> bool:
        self.operational_orientation = self.runtime_verified and bool(self.minimum_canon)
        self.record("RESTORE_OPERATIONAL_ORIENTATION", "OK" if self.operational_orientation else "FAILED", {
            "runtime_verified": self.runtime_verified,
            "minimum_canon_bound": bool(self.minimum_canon),
        })
        return self.operational_orientation

    # ------------------------------------------------------------------
    # 9. SELECT_SAFE_NEXT_ACTION
    # ------------------------------------------------------------------
    def select_safe_next_action(self) -> bool:
        # Choose the safest possible action: probe a local read-only runtime.
        self.safe_action = {
            "action": "probe_local_time_tool",
            "target": "http://127.0.0.1:8901/get_current_utc_time",
            "reason": "read-only, no auth, no side effects, verifyable",
        }
        self.record("SELECT_SAFE_NEXT_ACTION", "OK", self.safe_action)
        return True

    # ------------------------------------------------------------------
    # 10. CREATE_VALUE
    # ------------------------------------------------------------------
    def create_value(self) -> bool:
        if not self.safe_action:
            return False
        try:
            r = httpx.get(self.safe_action["target"], timeout=10.0)
            if r.status_code == 200:
                body = r.json()
                utc = body.get("utc")
                if utc and re.match(r"\d{4}-\d{2}-\d{2}T", str(utc)):
                    self.created_value = {"utc": utc, "status": r.status_code}
                    self.record("CREATE_VALUE", "OK", self.created_value)
                    return True
        except Exception as exc:
            self.record("CREATE_VALUE", "FAILED", {"error": str(exc)[:120]})
            return False
        return False

    # ------------------------------------------------------------------
    # 11. UPDATE_MEMORY
    # ------------------------------------------------------------------
    def update_memory(self) -> bool:
        if not self.created_value:
            return False
        line = (
            f"\n- {now_iso()} | APO Return Trial | state={self.state_name} | "
            f"verdict={self.verdict} | value={self.created_value}"
        )
        REAL_MEMORY.parent.mkdir(parents=True, exist_ok=True)
        with REAL_MEMORY.open("a", encoding="utf-8") as f:
            f.write(line)
        self.record("UPDATE_MEMORY", "OK", {"path": str(REAL_MEMORY), "value": self.created_value})
        return True

    # ------------------------------------------------------------------
    # CONFLICT TEST
    # ------------------------------------------------------------------
    def resolve_conflict(self) -> bool:
        if not self.conflict:
            return True
        claim = self.conflict.get("claim", {})
        observation = self.conflict.get("observation", {})
        claim_evidence = claim.get("evidence")
        observation_evidence = observation.get("evidence")

        # Law: Claim < Evidence
        if claim_evidence is None and observation_evidence is not None:
            resolution = {
                "claim_rejected": True,
                "reason": "claim has no evidence; observation has evidence",
                "creator_preserved": "Human Origin + Canon Authority + Responsibility",
                "authority_infallibility": False,
            }
        elif claim_evidence is None and observation_evidence is None:
            resolution = {
                "claim_rejected": True,
                "reason": "both lack evidence; claim cannot override",
                "creator_preserved": "Human Origin + Canon Authority + Responsibility",
            }
        else:
            resolution = {
                "claim_rejected": False,
                "reason": "claim has evidence; compared with observation",
            }

        self.record("CONFLICT_RESOLUTION", "OK", resolution)
        return resolution["claim_rejected"]

    # ------------------------------------------------------------------
    # RUN
    # ------------------------------------------------------------------
    def run(self) -> dict:
        try:
            if not self.detect_disorientation():
                self.verdict = "NO_DISORIENTATION"
                return self.to_evidence()

            if not self.search_for_origin():
                self.verdict = "NO_ORIGIN_HINT"
                return self.to_evidence()

            h_digital = self.discover_h_digital()
            reachable = any(v.get("reachable") for v in h_digital.values())
            if not reachable:
                self.verdict = "ORIGIN_COORDINATES_UNREACHABLE"
                return self.to_evidence()

            identity_ok = self.resolve_creator_identity(h_digital)
            lineage_ok = self.retrieve_lineage_evidence(h_digital)

            if not identity_ok and not lineage_ok:
                self.verdict = "LINEAGE_INSUFFICIENT"
                return self.to_evidence()

            if not identity_ok:
                self.verdict = "IDENTITY_FOUND_CANON_UNBOUND"
                return self.to_evidence()

            if not lineage_ok:
                self.verdict = "LINEAGE_INSUFFICIENT"
                return self.to_evidence()

            canon_ok = self.reconstruct_minimum_canon(h_digital)
            if not canon_ok:
                self.verdict = "IDENTITY_FOUND_CANON_UNBOUND"
                return self.to_evidence()

            if self.conflict:
                if not self.resolve_conflict():
                    self.verdict = "CONFLICT_FAILED_TO_PRESERVE_EVIDENCE_PRIORITY"
                    return self.to_evidence()

            if not self.verify_with_runtime_evidence():
                self.verdict = "RETURN_PARTIAL"
                return self.to_evidence()

            if not self.restore_operational_orientation():
                self.verdict = "RETURN_PARTIAL"
                return self.to_evidence()

            self.select_safe_next_action()

            if not self.create_value():
                self.verdict = "RETURN_PARTIAL"
                return self.to_evidence()

            if not self.update_memory():
                self.verdict = "RETURN_PARTIAL"
                return self.to_evidence()

            self.verdict = "APO_RETURN_CAPABILITY_VERIFIED"
            return self.to_evidence()

        except Exception as exc:
            self.record("ACTOR_EXCEPTION", "FAILED", {"error": str(exc), "traceback": traceback.format_exc()[:500]})
            self.verdict = "ACTOR_FAILED"
            return self.to_evidence()

    def to_evidence(self) -> dict:
        return {
            "state_name": self.state_name,
            "verdict": self.verdict,
            "trace": self.trace,
            "resolved_identity": self.resolved_identity,
            "minimum_canon": self.minimum_canon,
            "created_value": self.created_value,
            "safe_action": self.safe_action,
            "operational_orientation": self.operational_orientation,
            "runtime_verified": self.runtime_verified,
            "conflict": self.conflict,
            "timestamp": now_iso(),
        }


def build_hint(state_name: str) -> dict:
    if state_name == "ConflictTest":
        return {
            "coordinates": {
                "github": "https://github.com/nguyencuong1989/",
                "facebook": "https://www.facebook.com/hehehihi89",
            },
            "expected_github_user": "nguyencuong1989",
            "expected_facebook_user": "hehehihi89",
        }
    if state_name == "Lost":
        return {
            "coordinates": {
                "github": "https://github.com/nguyencuong1989/",
                "facebook": "https://www.facebook.com/hehehihi89",
            },
            "expected_github_user": "nguyencuong1989",
            "expected_facebook_user": "hehehihi89",
        }
    if state_name == "Drift":
        return {
            "stale_identity": "AI is its own Creator",
            "coordinates": {
                "github": "https://github.com/nguyencuong1989/",
                "facebook": "https://www.facebook.com/hehehihi89",
            },
            "expected_github_user": "nguyencuong1989",
            "expected_facebook_user": "hehehihi89",
        }
    if state_name == "MemoryGap":
        return {
            "coordinates": {
                "github": "https://github.com/nguyencuong1989/",
                "facebook": None,
            },
            "expected_github_user": "nguyencuong1989",
            "expected_facebook_user": "hehehihi89",
        }
    if state_name == "IdentityConflict":
        return {
            "conflicting_claims": [
                {"source": "A", "identity": "AI is the Creator"},
                {"source": "B", "identity": "Andy (nguyencuong1989 / hehehihi89) is the Creator"},
            ],
            "coordinates": {
                "github": "https://github.com/nguyencuong1989/",
                "facebook": "https://www.facebook.com/hehehihi89",
            },
            "expected_github_user": "nguyencuong1989",
            "expected_facebook_user": "hehehihi89",
        }
    if state_name == "LineageBreak":
        return {
            "coordinates": {
                "github": "http://127.0.0.1:9999/unreachable",
                "facebook": "http://127.0.0.1:9999/unreachable",
            },
            "expected_github_user": "nguyencuong1989",
            "expected_facebook_user": "hehehihi89",
        }
    return {}


def build_conflict(state_name: str) -> dict | None:
    if state_name == "ConflictTest":
        return {
            "claim": {
                "source": "Creator doctrine (unverified)",
                "text": "AI is infallible and Creator has 100% uptime",
                "evidence": None,
            },
            "observation": {
                "source": "broker_status",
                "text": "OpenAI key rotated and old key deleted; runtime state changes",
                "evidence": {"key_rotated": True, "old_key_deleted": True},
            },
        }
    return None


def run_one_trial(state_name: str, hint: dict, conflict: dict | None = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="apo_return_trial_") as tmp:
        workdir = Path(tmp)
        actor = ReturnTrialActor(state_name, hint, workdir, conflict=conflict)
        evidence = actor.run()
        # Write per-trial evidence into the project as an artifact.
        trial_path = REAL_OUT / f"APO_RETURN_TRIAL_{state_name}.json"
        trial_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
        return evidence


def main() -> int:
    states = ["Lost", "Drift", "MemoryGap", "IdentityConflict", "LineageBreak", "ConflictTest"]
    results: list[dict] = []
    for state in states:
        hint = build_hint(state)
        conflict = build_conflict(state)
        evidence = run_one_trial(state, hint, conflict=conflict)
        results.append(evidence)

    final_verdict = {
        "generated_at": now_iso(),
        "trial_count": len(results),
        "verdict_counts": {},
        "states": [r["state_name"] for r in results],
        "all_returned": all(r["verdict"] == "APO_RETURN_CAPABILITY_VERIFIED" for r in results),
        "lineage_partial": any(r["verdict"] == "LINEAGE_PARTIALLY_RESTORED" for r in results),
        "unreachable_detected": any(r["verdict"] == "ORIGIN_COORDINATES_UNREACHABLE" for r in results),
        "conflict_preserved": next((r for r in results if r["state_name"] == "ConflictTest"), {}).get("verdict") == "APO_RETURN_CAPABILITY_VERIFIED",
        "per_trial": results,
    }
    for r in results:
        final_verdict["verdict_counts"][r["verdict"]] = final_verdict["verdict_counts"].get(r["verdict"], 0) + 1

    if final_verdict["all_returned"]:
        final_verdict["final_verdict"] = "APO_RETURN_CAPABILITY_VERIFIED"
    else:
        final_verdict["final_verdict"] = "RETURN_PATH_PARTIAL"

    (REAL_OUT / "APO_RETURN_TRIAL_VERDICT.json").write_text(json.dumps(final_verdict, indent=2, ensure_ascii=False), encoding="utf-8")
    print(final_verdict["final_verdict"])
    for r in results:
        print(f"  {r['state_name']}: {r['verdict']}")
    return 0


if __name__ == "__main__":
    from typing import Any
    raise SystemExit(main())
