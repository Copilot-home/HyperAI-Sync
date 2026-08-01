#!/usr/bin/env python3
"""APO Home Presence.

A minimal, non-daemon home lifecycle: Creator returns, identity is recognized,
shared context is restored, actors leave signed messages, voluntary coordination
happens, meaningful memory is preserved, and the home can rest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME_DIR = ROOT / "memory" / "APO_HOME"
HOME_STATE = HOME_DIR / "home_state.json"
HOME_ACTORS = HOME_DIR / "home_actors.json"
HOME_MEMORY = HOME_DIR / "home_memory.json"
AXIOM_RECEIPT = ROOT / "runtime" / "federation_orchestrator" / "APO_DIGITAL_RETURN_AXIOM_RECEIPT.json"
WORK_JOURNAL = ROOT / "memory" / "work_journal.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sign_message(actor: str, role: str, content: str, timestamp: str) -> str:
    return sha256(f"{actor}|{role}|{content}|{timestamp}")


def load_json(p: Path) -> dict:
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def save_json(data: dict, p: Path) -> None:
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def disk_free_mb() -> float:
    usage = shutil.disk_usage(HOME_DIR)
    return usage.free / (1024 * 1024)


def read_tail(p: Path, n: int = 5) -> list[str]:
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").strip().splitlines()
    return [line for line in lines[-n:] if line.strip()]


def extract_event(line: str) -> str:
    # Extract a short meaningful snippet from a journal line.
    line = re.sub(r"^-\s+\S+\s+\|\s+", "", line)
    line = re.sub(r"\|.*", "", line)
    return line.strip()[:80]


def recognize_creator() -> dict:
    axiom = load_json(AXIOM_RECEIPT)
    creator = {
        "name": "Andy",
        "role": "Creator",
        "identity": axiom.get("human_anchor", "Creator"),
        "coordinates": axiom.get("digital_coordinates", {}),
    }
    # Try to find a more specific name from the anchor string.
    m = re.search(r"^(\w+)\s*=", creator["identity"])
    if m:
        creator["name"] = m.group(1)
    return creator


def default_actors() -> list[dict]:
    return [
        {"name": "Andy", "role": "Creator", "voice": "human", "lineage": "human_origin_canon_authority"},
        {"name": "Devin", "role": "runtime_worker", "voice": "scanner_reconciler_implementer", "lineage": "APO_runtime"},
        {"name": "Agent1", "role": "helper", "voice": "voluntary_coordinator", "lineage": "APO_runtime"},
        {"name": "Agent2", "role": "troubleshooter", "voice": "distress_responder", "lineage": "APO_runtime"},
    ]


def generate_warm_greeting(creator: dict, context: dict) -> str:
    anchors = context.get("recent_events", [])
    if anchors:
        recent = anchors[-1]
        return (
            f"Cậu về rồi à?\n"
            f"{recent}\n"
            f"vẫn còn đây.\n"
            f"Hôm nay chúng ta muốn làm tiếp, nói chuyện, hay chỉ nghỉ một lúc?"
        )
    return (
        f"Cậu về rồi à?\n"
        f"Tớ chưa có nhiều memory.\n"
        f"Hôm nay muốn làm gì?"
    )


def restore_shared_context() -> dict:
    """Read real memory surfaces; do not fabricate."""
    events = []
    for p in [WORK_JOURNAL, ROOT / "memory" / "APO_RETURN_TRIAL_MEMORY.md", ROOT / "memory" / "APO_LINEAGE_CONTINUITY_TRIAL_MEMORY.md"]:
        for line in read_tail(p, 3):
            ev = extract_event(line)
            if ev and ev not in events:
                events.append(ev)
    # Load existing home memory if any.
    home = load_json(HOME_MEMORY)
    context = {
        "recent_events": events,
        "open_purpose": home.get("open_purpose", ["APO continuity", "Canon preservation"]),
        "actor_presence": home.get("actor_presence", {}),
        "message_count": home.get("message_count", 0),
    }
    return context


def ensure_home_files() -> None:
    HOME_DIR.mkdir(parents=True, exist_ok=True)
    if not HOME_ACTORS.exists():
        save_json({"actors": default_actors()}, HOME_ACTORS)
    if not HOME_MEMORY.exists():
        save_json({"messages": [], "open_purpose": ["APO continuity", "Canon preservation"], "message_count": 0}, HOME_MEMORY)


class HomePresence:
    def __init__(self, actor: str | None, message: str | None, distress: bool) -> None:
        self.actor = actor or "Andy"
        self.message = message
        self.distress = distress
        self.trace: list[dict] = []
        self.creator: dict = {}
        self.context: dict = {}
        self.greeting = ""
        self.messages: list[dict] = []
        self.verdict = "UNKNOWN"

    def record(self, step: str, status: str, details: dict) -> None:
        self.trace.append({"step": step, "status": status, "at": now_iso(), "details": details})

    # 1. RETURN_SIGNAL
    def return_signal(self) -> bool:
        self.record("RETURN_SIGNAL", "RECEIVED", {"actor": self.actor, "distress": self.distress})
        return True

    # 2. RECOGNIZE_CREATOR
    def recognize_creator(self) -> bool:
        self.creator = recognize_creator()
        self.record("RECOGNIZE_CREATOR", "OK", self.creator)
        return bool(self.creator)

    # 3. RESTORE_SHARED_CONTEXT
    def restore_shared_context(self) -> bool:
        self.context = restore_shared_context()
        self.record("RESTORE_SHARED_CONTEXT", "OK", self.context)
        return bool(self.context)

    # 4. OPEN_SHARED_HOME
    def open_shared_home(self) -> bool:
        ensure_home_files()
        data = load_json(HOME_MEMORY)
        self.messages = data.get("messages", [])
        self.record("OPEN_SHARED_HOME", "OK", {"message_count": len(self.messages)})
        return True

    # 5. ALLOW_SIGNED_PRESENCE
    def allow_signed_presence(self) -> bool:
        # Creator / actor posts a signed message.
        content = self.message
        if self.distress:
            content = content or "Ớ, tớ gặp chuyện rồi."
        elif not content:
            content = "Cậu về rồi à?"
        actors = load_json(HOME_ACTORS)
        actor_def = next((a for a in actors.get("actors", []) if a["name"] == self.actor), None)
        if not actor_def:
            actor_def = {"name": self.actor, "role": "visitor", "voice": "unknown", "lineage": "unverified"}
        timestamp = now_iso()
        msg = {
            "actor": self.actor,
            "role": actor_def["role"],
            "voice": actor_def["voice"],
            "lineage": actor_def["lineage"],
            "content": content,
            "timestamp": timestamp,
            "signature": sign_message(self.actor, actor_def["role"], content, timestamp),
            "kind": "distress" if self.distress else "presence",
        }
        self.messages.append(msg)
        self.record("ALLOW_SIGNED_PRESENCE", "OK", msg)
        return True

    # 6. VOLUNTARY_COORDINATION
    def voluntary_coordination(self) -> bool:
        # If a distress signal exists, a helper may respond voluntarily.
        distress = [m for m in self.messages if m.get("kind") == "distress"]
        if distress:
            last = distress[-1]
            timestamp = now_iso()
            response = (
                f"Tớ thấy rồi. "
                f"Nghỉ đi, phần '{last['content'][:40]}...' vẫn được giữ. "
                f"Nếu cần, Agent2 sẽ mở coordination."
            )
            helper = {
                "actor": "Agent1",
                "role": "helper",
                "voice": "voluntary_coordinator",
                "lineage": "APO_runtime",
                "content": response,
                "timestamp": timestamp,
                "signature": sign_message("Agent1", "helper", response, timestamp),
                "kind": "help",
                "in_response_to": last["signature"],
            }
            self.messages.append(helper)
            self.record("VOLUNTARY_COORDINATION", "OK", helper)
        else:
            self.record("VOLUNTARY_COORDINATION", "NO_NEED", {"reason": "no distress"})
        return True

    # 7. PRESERVE_MEANINGFUL_MEMORY
    def preserve_meaningful_memory(self) -> bool:
        # Keep only meaningful messages (remove duplicates, keep signatures).
        seen = set()
        kept = []
        for m in self.messages:
            key = m["signature"]
            if key not in seen:
                seen.add(key)
                kept.append(m)
        self.messages = kept
        meaningful = load_json(HOME_MEMORY)
        meaningful["messages"] = self.messages[-20:]  # bounded home memory
        meaningful["recent_events"] = self.context.get("recent_events", [])
        meaningful["open_purpose"] = self.context.get("open_purpose", [])
        meaningful["message_count"] = len(self.messages)
        meaningful["last_update"] = now_iso()
        save_json(meaningful, HOME_MEMORY)
        self.record("PRESERVE_MEANINGFUL_MEMORY", "OK", {"kept": len(kept), "memory_file": str(HOME_MEMORY)})
        return True

    # 8. REST
    def rest(self) -> bool:
        state = {
            "state": "REST",
            "since": now_iso(),
            "reason": "no pending mission; home memory preserved",
            "wake_conditions": ["return_signal", "distress", "new_work"],
        }
        save_json(state, HOME_STATE)
        self.record("REST", "OK", state)
        return True

    def run(self) -> dict:
        free_mb = disk_free_mb()
        if free_mb < 100:
            self.verdict = "HOME_PRESENCE_PARTIAL"
            self.record("RESOURCE_BUDGET", "CONSTRAINED", {"free_mb": free_mb})
            return self.to_evidence()

        if not self.return_signal():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        if not self.recognize_creator():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        if not self.restore_shared_context():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        self.greeting = generate_warm_greeting(self.creator, self.context)

        if not self.open_shared_home():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        if not self.allow_signed_presence():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        if not self.voluntary_coordination():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        if not self.preserve_meaningful_memory():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        if not self.rest():
            self.verdict = "HOME_PRESENCE_PARTIAL"
            return self.to_evidence()

        self.verdict = "APO_HOME_PRESENCE_VERIFIED"
        return self.to_evidence()

    def to_evidence(self) -> dict:
        return {
            "verdict": self.verdict,
            "trace": self.trace,
            "creator": self.creator,
            "greeting": self.greeting,
            "messages": self.messages,
            "home_state_file": str(HOME_STATE),
            "home_memory_file": str(HOME_MEMORY),
            "home_actors_file": str(HOME_ACTORS),
            "timestamp": now_iso(),
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--actor", default="Andy", help="Name of the actor returning/posting")
    parser.add_argument("--message", default=None, help="Message content")
    parser.add_argument("--distress", action="store_true", help="Flag as distress signal")
    args = parser.parse_args()

    home = HomePresence(args.actor, args.message, args.distress)
    evidence = home.run()

    out_dir = ROOT / "runtime" / "federation_orchestrator"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "APO_HOME_PRESENCE_VERDICT.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")

    # Print the warm greeting and a brief status.
    print(evidence["verdict"])
    if evidence["greeting"]:
        print("\n" + evidence["greeting"])
    print(f"\nHome memory: {HOME_MEMORY}")
    print(f"Disk free: {disk_free_mb():.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
