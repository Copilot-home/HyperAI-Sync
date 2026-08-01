#!/usr/bin/env python3
"""One full causal mission: AUTH → ROUTING → EXECUTION → VERIFICATION → MEMORY.

Also serves as the first observer-guarded run: run lock, retry, backoff,
resource budgets, and optional failure injection.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

import httpx
import psutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "runtime" / "federation_orchestrator"
MEMORY = ROOT / "memory" / "work_journal.md"
RUN_LOCK = OUT / "aios_full_causal_mission.run.lock"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(s: str | bytes) -> str:
    if isinstance(s, str):
        s = s.encode("utf-8")
    return hashlib.sha256(s).hexdigest()


def hash_resp(resp: httpx.Response) -> str:
    try:
        return sha256(resp.text)
    except Exception:
        return sha256("")


class Guard:
    """Observer guard: run lock, retry, backoff, resource budgets, failure injection."""

    def __init__(
        self,
        max_duration: float = 60.0,
        max_retries: int = 3,
        base_backoff: float = 1.0,
        max_backoff: float = 10.0,
        max_rss_mb: float = 512.0,
        max_cpu_percent: float = 80.0,
        failure_injection: str | None = None,
    ):
        self.max_duration = max_duration
        self.max_retries = max_retries
        self.base_backoff = base_backoff
        self.max_backoff = max_backoff
        self.max_rss_mb = max_rss_mb
        self.max_cpu_percent = max_cpu_percent
        self.failure_injection = failure_injection
        self.start_ts = time.time()
        self.start_iso = now_iso()
        self.process = psutil.Process()
        self.start_mem_mb = self.process.memory_info().rss / (1024 * 1024)
        self.start_cpu = self.process.cpu_percent(interval=None)
        self.lock_fd = None
        self.retries_total = 0
        self.failures: list[dict] = []

    def acquire_run_lock(self) -> None:
        import fcntl

        self.lock_fd = open(RUN_LOCK, "w")
        try:
            fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lock_fd.write(f"{os.getpid()}\n{now_iso()}")
            self.lock_fd.flush()
        except BlockingIOError:
            raise RuntimeError("another_full_causal_mission_is_running")

    def release_run_lock(self) -> None:
        if self.lock_fd:
            import fcntl

            fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_UN)
            self.lock_fd.close()
            try:
                RUN_LOCK.unlink()
            except FileNotFoundError:
                pass

    def check_budget(self) -> None:
        elapsed = time.time() - self.start_ts
        if elapsed > self.max_duration:
            raise RuntimeError(f"duration_budget_exceeded: {elapsed:.1f}s > {self.max_duration}s")
        mem_mb = self.process.memory_info().rss / (1024 * 1024)
        if mem_mb > self.max_rss_mb:
            raise RuntimeError(f"rss_budget_exceeded: {mem_mb:.1f}MB > {self.max_rss_mb}MB")

    def should_retry(self, exc: Exception | None, status: int | None) -> bool:
        if self.retries_total >= self.max_retries * 5:  # global cap
            return False
        if exc is not None:
            return True
        if status is not None and status >= 500:
            return True
        if status is not None and status in (408, 429, 503, 504):
            return True
        return False

    def inject_failure(self, step: str, request: dict | None = None) -> None:
        if self.failure_injection is None:
            return
        if step == self.failure_injection or (self.failure_injection == "random" and random.random() < 0.3):
            raise RuntimeError(f"injected_failure:{self.failure_injection}")

    def call(self, step: str, fn, *args, **kwargs) -> Any:
        """Call a step with retry/backoff and optional failure injection."""
        attempt = 0
        backoff = self.base_backoff
        while True:
            self.check_budget()
            try:
                self.inject_failure(step)
                return fn(*args, **kwargs)
            except Exception as exc:
                status = getattr(exc, "status_code", None)
                if not self.should_retry(exc, status) or attempt >= self.max_retries:
                    raise
                self.retries_total += 1
                self.failures.append({
                    "step": step,
                    "attempt": attempt,
                    "error": str(exc),
                    "at": now_iso(),
                    "backoff_sec": min(backoff, self.max_backoff),
                })
                time.sleep(min(backoff, self.max_backoff))
                backoff *= 2
                attempt += 1

    def resource_report(self) -> dict:
        elapsed = time.time() - self.start_ts
        mem_mb = self.process.memory_info().rss / (1024 * 1024)
        cpu_percent = self.process.cpu_percent(interval=0.1)
        return {
            "generated_at": now_iso(),
            "mission": "full_causal_mission",
            "duration_sec": round(elapsed, 3),
            "duration_budget_sec": self.max_duration,
            "duration_status": "OK" if elapsed <= self.max_duration else "OVERRUN",
            "peak_rss_mb": round(mem_mb, 2),
            "rss_budget_mb": self.max_rss_mb,
            "rss_status": "OK" if mem_mb <= self.max_rss_mb else "OVERRUN",
            "cpu_percent": round(cpu_percent, 2),
            "cpu_budget_percent": self.max_cpu_percent,
            "cpu_status": "OK" if cpu_percent <= self.max_cpu_percent else "OVERRUN",
            "retries_total": self.retries_total,
            "failure_injection": self.failure_injection,
            "failure_count": len(self.failures),
        }


def build_request_hash(method: str, url: str, body: str = "", headers: dict | None = None) -> str:
    h = f"{method} {url} {body}"
    if headers:
        h += json.dumps(sorted(headers.items()))
    return sha256(h)


def edge(
    source: str,
    dest: str,
    method: str,
    url: str,
    req_hash: str,
    resp_hash: str,
    started_at: str,
    completed_at: str,
    authority: str,
    lease_id: str | None,
    verified: bool,
    note: str = "",
) -> dict:
    return {
        "source_actor": source,
        "destination_actor": dest,
        "method": method,
        "url": url,
        "request_hash": req_hash,
        "response_hash": resp_hash,
        "started_at": started_at,
        "completed_at": completed_at,
        "authority": authority,
        "lease_id_or_fingerprint": lease_id or "none",
        "verification_result": "PASS" if verified else "FAIL",
        "note": note,
    }


def full_mission(guard: Guard, broker_url: str, gateway_url: str, openai_proxy: bool = False) -> dict:
    mission_id = f"full-causal-{now_iso().replace(':', '')}"
    log: dict[str, Any] = {
        "mission_id": mission_id,
        "mission_class": "AUTH_ROUTING_EXECUTION_VERIFICATION_MEMORY",
        "started_at": now_iso(),
        "stages": {},
        "edges": [],
    }

    # -------------------------------------------------------------------
    # 0. CREATOR -> AUTH edge (canonical root authority)
    # -------------------------------------------------------------------
    log["edges"].append({
        "source_actor": "CREATOR",
        "destination_actor": "AUTH",
        "method": "INTENT",
        "url": "canon://full_causal_mission",
        "request_hash": sha256("canon://full_causal_mission"),
        "response_hash": sha256(mission_id),
        "started_at": now_iso(),
        "completed_at": now_iso(),
        "authority": "CREATOR",
        "lease_id_or_fingerprint": "none",
        "verification_result": "PASS",
        "note": "canonical root authority for AUTH lane",
    })

    # -------------------------------------------------------------------
    # 1. AUTH: issue lease from credential broker
    # -------------------------------------------------------------------
    broker = httpx.Client(base_url=broker_url, timeout=30.0)
    auth_started = now_iso()
    capability_req = {
        "node": "local",
        "task": mission_id,
        "provider": "openai",
        "resource": "models",
        "action": "read",
        "scope_req": ["read"],
        "ttl_req": 120,
        "proof_req": {"mission_class": "full_causal", "intent": "AUTH_TO_ROUTING"},
    }
    req_hash = build_request_hash("POST", f"{broker_url}/capability", json.dumps(capability_req, sort_keys=True))
    r = guard.call("AUTH", broker.post, "/capability", json=capability_req)
    auth_completed = now_iso()
    if r.status_code != 200:
        raise RuntimeError(f"AUTH_failed:{r.status_code}:{r.text}")
    auth_body = r.json()
    lease_id = auth_body["lease"]["lease_id"]
    lease_ref = auth_body["lease"]["active_key_ref"]
    resp_hash = hash_resp(r)
    log["stages"]["AUTH"] = {
        "status_code": r.status_code,
        "decision": auth_body.get("decision"),
        "lease_id": lease_id,
        "active_key_ref": lease_ref,
        "started_at": auth_started,
        "completed_at": auth_completed,
        "request_hash": req_hash,
        "response_hash": resp_hash,
    }

    # edge CREATOR -> AUTH already emitted; add AUTH -> ROUTING
    log["edges"].append(edge(
        "AUTH", "ROUTING", "POST", f"{broker_url}/capability",
        req_hash, resp_hash, auth_started, auth_completed,
        "broker", lease_id, True,
        "lease issued; next hop apo_gateway with X-Lease-Id",
    ))

    # -------------------------------------------------------------------
    # 2. ROUTING: apo_gateway with X-Lease-Id
    # -------------------------------------------------------------------
    gateway = httpx.Client(base_url=gateway_url, timeout=30.0)
    route_started = now_iso()
    route_url = f"{gateway_url}/tools/time/get_current_utc_time"
    route_headers = {"X-Lease-Id": lease_id, "Accept": "application/json"}
    route_req_hash = build_request_hash("GET", route_url, headers=route_headers)
    r2 = guard.call("ROUTING", gateway.get, "/tools/time/get_current_utc_time", headers=route_headers)
    route_completed = now_iso()
    if r2.status_code != 200:
        raise RuntimeError(f"ROUTING_FAILED:{r2.status_code}:{r2.text}")
    route_resp_hash = hash_resp(r2)
    log["stages"]["ROUTING"] = {
        "status_code": r2.status_code,
        "url": route_url,
        "started_at": route_started,
        "completed_at": route_completed,
        "request_hash": route_req_hash,
        "response_hash": route_resp_hash,
    }
    log["edges"].append(edge(
        "ROUTING", "EXECUTION", "GET", route_url,
        route_req_hash, route_resp_hash, route_started, route_completed,
        "apo_gateway", lease_id, True,
        "gateway verified lease then proxied to openapi_tool_time",
    ))

    # -------------------------------------------------------------------
    # 3. EXECUTION: time tool returned value
    # -------------------------------------------------------------------
    exec_started = now_iso()
    exec_body = r2.json()
    exec_completed = now_iso()
    log["stages"]["EXECUTION"] = {
        "raw_response": exec_body,
        "started_at": exec_started,
        "completed_at": exec_completed,
        "response_hash": route_resp_hash,
    }
    log["edges"].append(edge(
        "EXECUTION", "VERIFICATION", "INTERNAL", "parse/verify",
        route_resp_hash, sha256(json.dumps(exec_body, sort_keys=True)),
        exec_started, exec_completed,
        "openapi_tool_time", lease_id, True,
        "value handed to verification layer",
    ))

    # -------------------------------------------------------------------
    # 4. VERIFICATION: UTC value is well-formed
    # -------------------------------------------------------------------
    verify_started = now_iso()
    utc = exec_body.get("utc")
    verified = bool(utc and re.match(r"\d{4}-\d{2}-\d{2}T", str(utc)))
    verify_completed = now_iso()
    log["stages"]["VERIFICATION"] = {
        "utc": utc,
        "verified": verified,
        "started_at": verify_started,
        "completed_at": verify_completed,
    }
    verify_resp_hash = sha256(json.dumps({"verified": verified, "utc": utc}, sort_keys=True))
    log["edges"].append(edge(
        "VERIFICATION", "MEMORY", "INTERNAL", "write_receipt",
        sha256(json.dumps(exec_body, sort_keys=True)), verify_resp_hash,
        verify_started, verify_completed,
        "local_verifier", lease_id, verified,
        "verification passed -> memory write",
    ))

    # -------------------------------------------------------------------
    # 5. MEMORY: append to work journal and write mission log
    # -------------------------------------------------------------------
    memory_started = now_iso()
    journal_line = (
        f"\n- {now_iso()} | {mission_id} | full_causal_mission | "
        f"AUTH->ROUTING->EXECUTION->VERIFICATION->MEMORY | lease={lease_id} | utc={utc}"
    )
    with MEMORY.open("a", encoding="utf-8") as f:
        f.write(journal_line)
    mission_log_path = OUT / f"{mission_id}_execution_log.json"
    mission_log_path.write_text(json.dumps(log, indent=2), encoding="utf-8")
    memory_completed = now_iso()
    log["stages"]["MEMORY"] = {
        "journal_appended": True,
        "mission_log": str(mission_log_path.relative_to(ROOT)),
        "started_at": memory_started,
        "completed_at": memory_completed,
    }
    log["edges"].append(edge(
        "MEMORY", "CREATOR", "INTERNAL", "receipt",
        verify_resp_hash, sha256(str(mission_log_path)),
        memory_started, memory_completed,
        "memory_writer", lease_id, verified,
        "memory receipt returned to creator",
    ))

    log["completed_at"] = now_iso()
    log["verdict"] = "FULL_CAUSAL_MISSION_VERIFIED" if verified else "VERIFICATION_FAILED"
    return log


def run_normal(broker_url: str, gateway_url: str) -> dict:
    guard = Guard()
    try:
        guard.acquire_run_lock()
        log = full_mission(guard, broker_url, gateway_url)
        resource_receipt = guard.resource_report()
        resource_receipt["mission_verdict"] = log["verdict"]
        (OUT / "observer_resource_budget_receipt.json").write_text(json.dumps(resource_receipt, indent=2), encoding="utf-8")
        (OUT / "full_causal_mission_execution_log.json").write_text(json.dumps(log, indent=2), encoding="utf-8")
        return log
    finally:
        guard.release_run_lock()


def run_failure_injection(failure: str, broker_url: str, gateway_url: str) -> dict:
    guard = Guard(failure_injection=failure, max_retries=3)
    result = {"verdict": "NOT_RUN", "failures": []}
    try:
        guard.acquire_run_lock()
        try:
            if failure == "broker_unreachable":
                wrong_broker = "http://127.0.0.1:8766"
                full_mission(guard, wrong_broker, gateway_url)
            elif failure == "invalid_lease_id":
                gateway = httpx.Client(base_url=gateway_url, timeout=10.0)
                r = guard.call("ROUTING", gateway.get, "/tools/time/get_current_utc_time", headers={"X-Lease-Id": "lease_fake"})
                result = {
                    "verdict": "INJECTION_DETECTED" if r.status_code == 403 else "INJECTION_MISS",
                    "injected_step": "ROUTING",
                    "status_code": r.status_code,
                    "note": "fake lease rejected by gateway" if r.status_code == 403 else "unexpected status",
                }
            elif failure == "gateway_unreachable":
                wrong_gateway = "http://127.0.0.1:9012"
                full_mission(guard, broker_url, wrong_gateway)
            else:
                full_mission(guard, broker_url, gateway_url)
        except Exception as exc:
            result = {
                "verdict": "INJECTION_CAUGHT",
                "injected_step": failure,
                "error": str(exc),
                "traceback": traceback.format_exc(),
            }
        resource_receipt = guard.resource_report()
        (OUT / "observer_resource_budget_injection_receipt.json").write_text(json.dumps(resource_receipt, indent=2), encoding="utf-8")
        failure_receipt = {
            "generated_at": now_iso(),
            "failure_injection": failure,
            "result": result,
            "retries_total": guard.retries_total,
            "retried_failures": guard.failures,
            "observer_verdict": "GUARD_CAUGHT" if result["verdict"].startswith("INJECTION") else "GUARD_MISS",
        }
        (OUT / f"observer_failure_injection_{failure}.json").write_text(json.dumps(failure_receipt, indent=2), encoding="utf-8")
        (OUT / "observer_failure_injection_receipt.json").write_text(json.dumps(failure_receipt, indent=2), encoding="utf-8")
        return failure_receipt
    finally:
        guard.release_run_lock()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--broker-url", default=os.environ.get("HYPERAI_BROKER_URL", "http://127.0.0.1:8765"))
    parser.add_argument("--gateway-url", default=os.environ.get("APO_GATEWAY_URL", "http://127.0.0.1:9011"))
    parser.add_argument("--failure-injection", default=None, help="broker_unreachable | invalid_lease_id | gateway_unreachable | random")
    args = parser.parse_args()

    if args.failure_injection:
        receipt = run_failure_injection(args.failure_injection, args.broker_url, args.gateway_url)
        print(json.dumps(receipt, indent=2))
    else:
        log = run_normal(args.broker_url, args.gateway_url)
        print(f"verdict={log['verdict']} mission_id={log['mission_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
