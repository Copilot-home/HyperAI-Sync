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

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any


ENDPOINTS = [
    ("GET", "/api/health", None),
    ("GET", "/api/symphony/status", None),
    ("POST", "/api/symphony/start", {}),
]


def fetch_json(base_url: str, method: str, path: str, payload: Any) -> tuple[int, Any]:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}{path}",
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        body = resp.read().decode("utf-8")
        parsed = json.loads(body) if body else None
        return resp.status, parsed


def snapshot(base_url: str) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for method, path, payload in ENDPOINTS:
        try:
            status, body = fetch_json(base_url, method, path, payload)
            results[path] = {"status_code": status, "body": body}
        except urllib.error.HTTPError as exc:
            error_body = exc.read().decode("utf-8")
            results[path] = {
                "status_code": exc.code,
                "body": error_body,
            }
        except Exception as exc:  # pragma: no cover - operational script
            results[path] = {
                "status_code": None,
                "body": f"error: {exc}",
            }
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authority", required=True, help="Authoritative base URL")
    parser.add_argument("--candidate", help="Candidate base URL")
    args = parser.parse_args()

    authority = snapshot(args.authority)
    output: dict[str, Any] = {"authority": authority}

    if args.candidate:
        candidate = snapshot(args.candidate)
        mismatches: list[dict[str, Any]] = []
        for _, path, _ in ENDPOINTS:
            authority_result = authority[path]
            candidate_result = candidate[path]
            if authority_result != candidate_result:
                mismatches.append(
                    {
                        "path": path,
                        "authority": authority_result,
                        "candidate": candidate_result,
                    }
                )
        output["candidate"] = candidate
        output["parity"] = {
            "ok": not mismatches,
            "mismatches": mismatches,
        }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())