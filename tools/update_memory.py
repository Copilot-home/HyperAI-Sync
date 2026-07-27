from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEMORY_DIR = ROOT / "memory"
STATE_PATH = MEMORY_DIR / "project_state.json"
SESSION_PATH = MEMORY_DIR / "session_memory.md"
JOURNAL_PATH = MEMORY_DIR / "work_journal.md"
NEXT_PATH = MEMORY_DIR / "next_actions.md"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {
        "last_updated": now_iso(),
        "current_focus": "",
        "latest_summary": "",
        "active_blockers": [],
        "next_actions": [],
    }


def write_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_session_memory(focus: str, summary: str, blocker: str | None, next_action: str | None) -> None:
    lines = [
        "# Session Memory",
        "",
        f"- Last updated: {now_iso()}",
        f"- Current focus: {focus}",
        f"- Latest summary: {summary}",
    ]
    if blocker:
        lines.append(f"- Active blocker: {blocker}")
    if next_action:
        lines.append(f"- Next action: {next_action}")
    SESSION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def append_journal(focus: str, summary: str, blocker: str | None, next_action: str | None) -> None:
    timestamp = now_iso()
    entry = [f"- {timestamp} | Focus: {focus} | Summary: {summary}"]
    if blocker:
        entry.append(f"  Blocker: {blocker}")
    if next_action:
        entry.append(f"  Next: {next_action}")
    with JOURNAL_PATH.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(entry) + "\n")


def write_next_actions(next_action: str | None) -> None:
    lines = ["# Next Actions", ""]
    if next_action:
        lines.append(f"- {next_action}")
    else:
        lines.append("- No next action provided.")
    NEXT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update lightweight workspace memory files.")
    parser.add_argument("--focus", required=True, help="Current work focus.")
    parser.add_argument("--summary", required=True, help="What changed or was learned.")
    parser.add_argument("--next", dest="next_action", help="Immediate next action.")
    parser.add_argument("--blocker", help="Current blocker, if any.")
    args = parser.parse_args()

    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    state["last_updated"] = now_iso()
    state["current_focus"] = args.focus
    state["latest_summary"] = args.summary
    state["active_blockers"] = [args.blocker] if args.blocker else []
    state["next_actions"] = [args.next_action] if args.next_action else []

    write_state(state)
    write_session_memory(args.focus, args.summary, args.blocker, args.next_action)
    append_journal(args.focus, args.summary, args.blocker, args.next_action)
    write_next_actions(args.next_action)

    print("Memory updated.")


if __name__ == "__main__":
    main()
