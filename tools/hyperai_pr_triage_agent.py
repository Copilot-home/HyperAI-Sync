#!/usr/bin/env python3
"""HyperAI PR Triage Agent.

Reusable ecosystem PR cleanup runner. Implements the HyperAI Runtime
Orchestrator bounded-action contract:

  MISSION -> SKILL_DISCOVERY -> SKILL_SELECTION -> SKILL_EXECUTION
  -> VERIFY -> CONTINUE_QUEUE

It is designed to run unattended for low-risk PR hygiene:

* Close junk / spam PRs.
* Close stale draft PRs (no update within --stale-days, conflicts/unknown).
* Close stale non-draft PRs that are blocked or have conflicts and no recent activity.
* Merge PRs that are clean, mergeable, checks SUCCESS, and not review-blocked.

All actions are recorded as evidence artifacts. By default the tool runs in
dry-run mode; pass --execute to mutate GitHub state.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "runtime" / "federation_orchestrator" / "agent_task_outputs"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _age_days(iso: str) -> int:
    return (datetime.now(timezone.utc) - datetime.fromisoformat(iso.replace("Z", "+00:00"))).days


def _gh_env() -> dict[str, str]:
    """Return environment where GITHUB_TOKEN env override is removed.

    If the environment contains an invalid GITHUB_TOKEN, gh falls back to the
    keyring-authenticated account. We do not want to leak or rely on a stale env token.
    """
    env = dict(os.environ)
    env.pop("GITHUB_TOKEN", None)
    return env


def _run(cmd: list[str], check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, capture_output=True, text=True, env=_gh_env(), check=check)


def fetch_open_prs(owners: list[str]) -> list[dict[str, Any]]:
    prs: list[dict[str, Any]] = []
    fields = "number,title,url,repository,isDraft,commentsCount,createdAt,updatedAt,labels,author"
    for owner in owners:
        res = _run(["gh", "search", "prs", "--owner", owner, "--state", "open", "--limit", "100", "--json", fields])
        if res.returncode != 0:
            print(f"WARN: failed to fetch PRs for {owner}: {res.stderr.strip()}", file=sys.stderr)
            continue
        prs.extend(json.loads(res.stdout))
    return prs


def fetch_pr_details(repo: str, number: int) -> dict[str, Any] | None:
    fields = (
        "number,title,url,createdAt,updatedAt,isDraft,mergeStateStatus,mergeable,"
        "statusCheckRollup,author,reviewDecision,headRefName,baseRefName,comments,labels"
    )
    res = _run(["gh", "pr", "view", "--repo", repo, str(number), "--json", fields])
    if res.returncode != 0:
        print(f"WARN: failed to fetch details for {repo}#{number}: {res.stderr.strip()}", file=sys.stderr)
        return None
    return json.loads(res.stdout)


def check_status(rollup: list[dict[str, Any]] | None) -> str:
    if not rollup:
        return "UNKNOWN"
    states = [c.get("state") for c in rollup if c.get("state")]
    if "FAILURE" in states:
        return "FAILURE"
    if "PENDING" in states:
        return "PENDING"
    if states and all(s == "SUCCESS" for s in states):
        return "SUCCESS"
    return "MIXED"


def _is_wip(title: str, draft: bool) -> bool:
    t = title.lower()
    return bool(draft) or t.startswith("[wip]") or t.startswith("(wip)") or " [wip]" in t or " (wip)" in t


def classify_pr(pr: dict[str, Any], stale_days: int) -> tuple[str, str]:
    """Return (category, reason)."""
    title = pr.get("title", "")
    draft = _is_wip(pr.get("title", ""), bool(pr.get("isDraft")))
    updated = pr.get("updatedAt") or pr.get("createdAt")
    age = _age_days(updated) if updated else 0
    merge = pr.get("mergeStateStatus") or "UNKNOWN"
    mergeable = str(pr.get("mergeable") or "UNKNOWN")
    checks = check_status(pr.get("statusCheckRollup"))
    review = pr.get("reviewDecision") or "NONE"

    # Junk / spam detection
    stripped = title.strip().lower()
    if stripped in ("hi", "hello", "test") or len(title.strip()) < 4:
        return "junk", "title is junk/spam"

    # Merge candidates: non-WIP, clean, passing checks, not review-blocked
    if (
        not draft
        and merge == "CLEAN"
        and mergeable == "MERGEABLE"
        and checks == "SUCCESS"
        and review != "REVIEW_REQUIRED"
    ):
        return "merge", "clean, mergeable, checks pass, no review required"

    stale = age >= stale_days

    # WIP (draft or title [WIP]) that is stale
    if draft and stale:
        if merge == "DIRTY" or mergeable == "CONFLICTING":
            return "stale-wip-conflict", f"WIP {age}d old with merge conflict"
        if merge in ("UNKNOWN", "UNSTABLE"):
            return "stale-wip-unstable", f"WIP {age}d old with unstable/unknown status"
        if checks == "FAILURE":
            return "stale-wip-failure", f"WIP {age}d old with failing checks"
        return "stale-wip", f"WIP {age}d old"

    # Stale non-WIP with blockers
    if not draft and stale:
        if merge == "DIRTY" or mergeable == "CONFLICTING":
            return "stale-conflict", f"PR {age}d old with merge conflict"
        if merge == "BLOCKED" and review == "REVIEW_REQUIRED":
            return "stale-review-blocked", f"PR {age}d old and review-blocked"
        if merge == "UNSTABLE" and checks == "SUCCESS":
            return "unstable-clean-checks", f"PR {age}d old, out of date but checks pass"

    # Active / needs manual review
    if checks == "FAILURE":
        return "ci-failure", "checks failing"
    if merge == "BLOCKED" and review == "REVIEW_REQUIRED":
        return "review-required", "review required"
    if merge == "DIRTY" or mergeable == "CONFLICTING":
        return "conflict", "merge conflict"
    if draft:
        return "wip-draft", "active WIP"
    return "manual-review", "needs manual triage"


def decide_action(pr: dict[str, Any], category: str, reason: str, stale_days: int) -> dict[str, Any] | None:
    """Return action dict or None for manual-review."""
    if category == "junk":
        return {"action": "close_pr", "reason": reason, "comment": f"Closing as junk/spam PR per ecosystem triage."}
    if category.startswith("stale-"):
        return {
            "action": "close_pr",
            "reason": reason,
            "comment": f"Closing stale PR (>={stale_days}d, {reason}) per ecosystem triage. Reopen if still relevant.",
        }
    if category == "merge":
        return {"action": "merge_pr", "reason": reason, "method": "squash"}
    if category == "unstable-clean-checks":
        # Out-of-date but otherwise healthy; try update-branch then merge.
        return {"action": "update_then_merge", "reason": reason, "method": "squash"}
    return None


def execute_action(repo: str, number: int, action: dict[str, Any]) -> dict[str, Any]:
    kind = action["action"]
    log: dict[str, Any] = {"repo": repo, "number": number, "action": kind, "status": 1, "stdout": "", "stderr": ""}
    if kind == "close_pr":
        cmd = ["gh", "pr", "close", "--repo", repo, str(number), "--comment", action["comment"]]
        res = _run(cmd)
        log.update({"status": res.returncode, "stdout": res.stdout.strip(), "stderr": res.stderr.strip()})
    elif kind == "merge_pr":
        subject = action.get("subject") or f"Merge PR #{number}"
        cmd = ["gh", "pr", "merge", "--repo", repo, str(number), f"--{action['method']}", "--subject", subject, "--body", ""]
        res = _run(cmd)
        log.update({"status": res.returncode, "stdout": res.stdout.strip(), "stderr": res.stderr.strip()})
    elif kind == "update_then_merge":
        # First try a plain merge; if it fails because the branch is unstable,
        # update the branch and enable auto-merge.
        res1 = _run(["gh", "pr", "merge", "--repo", repo, str(number), f"--{action['method']}", "--subject", f"Merge PR #{number}", "--body", ""])
        if res1.returncode == 0:
            log.update({"status": 0, "stdout": res1.stdout.strip(), "stderr": res1.stderr.strip()})
        else:
            res2 = _run(["gh", "pr", "update-branch", "--repo", repo, str(number)])
            if res2.returncode == 0:
                res3 = _run(["gh", "pr", "merge", "--repo", repo, str(number), f"--{action['method']}", "--subject", f"Merge PR #{number}", "--body", ""])
                log.update({"status": res3.returncode, "stdout": res3.stdout.strip(), "stderr": res3.stderr.strip()})
            else:
                log.update({"status": res2.returncode, "stdout": res2.stdout.strip(), "stderr": res2.stderr.strip()})
    return log


def main() -> int:
    parser = argparse.ArgumentParser(description="HyperAI PR Triage Agent")
    parser.add_argument("--owners", nargs="+", help="GitHub owners to scan", default=["NguyenCuong1989", "Copilot-home"])
    parser.add_argument("--stale-days", type=int, default=90, help="Age threshold for stale PRs")
    parser.add_argument("--execute", action="store_true", help="Actually mutate PRs (default dry-run)")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT, help="Directory for evidence artifacts")
    parser.add_argument("--mission-id", help="HyperAI mission id to tag evidence")
    args = parser.parse_args()

    mission_id = args.mission_id or f"mission-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
    output_dir = args.output_dir / mission_id
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = output_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    print(f"MISSION_PACKET")
    print(f"  objective: ecosystem PR triage and low-risk cleanup")
    print(f"  target_surface: github_pull_requests")
    print(f"  risk_class: bounded_write")
    print(f"  requested_action: classify_and_cleanup")
    print(f"  approval_state: {'execute-approved' if args.execute else 'dry-run'}")
    print(f"SKILL_ROUTING_TABLE")
    print(f"  selected: hyperai_pr_triage_agent, gh CLI")
    print(f"  fallback: manual review for non-low-risk items")
    print(f"MEMORY_CONTEXT")
    print(f"  canon: HyperAI Runtime Orchestrator / bounded-action contract")
    print(f"  evidence_dir: {evidence_dir}")

    prs = fetch_open_prs(args.owners)
    (evidence_dir / "open_prs.json").write_text(json.dumps(prs, indent=2) + "\n", encoding="utf-8")
    print(f"ACTION_PACKET")
    print(f"  read: fetched {len(prs)} open PRs")

    classified: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    manual_review: list[dict[str, Any]] = []
    execution_log: list[dict[str, Any]] = []

    for pr in prs:
        repo = pr["repository"]["nameWithOwner"]
        number = pr["number"]
        details = fetch_pr_details(repo, number)
        if not details:
            # Fall back to search metadata
            details = pr
        category, reason = classify_pr(details, args.stale_days)
        action = decide_action(details, category, reason, args.stale_days)
        item = {
            "repo": repo,
            "number": number,
            "title": details.get("title", ""),
            "url": details.get("url", ""),
            "updated_age_days": _age_days(details.get("updatedAt") or details.get("createdAt")),
            "draft": details.get("isDraft"),
            "merge": details.get("mergeStateStatus"),
            "mergeable": str(details.get("mergeable")),
            "checks": check_status(details.get("statusCheckRollup")),
            "review": details.get("reviewDecision"),
            "category": category,
            "reason": reason,
            "proposed_action": action,
        }
        classified.append(item)
        if action:
            actions.append({**item, "action": action})
            if args.execute:
                log = execute_action(repo, number, action)
                item["execution"] = log
                execution_log.append(log)
        else:
            manual_review.append(item)

    closed = sum(1 for log in execution_log if log.get("status") == 0 and log.get("action") == "close_pr")
    merged = sum(1 for log in execution_log if log.get("status") == 0 and log.get("action") in ("merge_pr", "update_then_merge"))

    report = {
        "schema_version": "2026-04-16.hyperai-pr-triage.v1",
        "mission_id": mission_id,
        "timestamp": _now(),
        "execute": args.execute,
        "stale_days": args.stale_days,
        "owners": args.owners,
        "summary": {
            "total": len(classified),
            "actions": len(actions),
            "closed": closed,
            "merged": merged,
            "manual_review": len(manual_review),
            "by_category": {}
        },
        "classified": classified,
        "manual_review": manual_review,
    }
    by_category: dict[str, int] = {}
    for c in classified:
        by_category[c["category"]] = by_category.get(c["category"], 0) + 1
    report["summary"]["by_category"] = by_category

    (output_dir / "triage_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    if execution_log:
        (output_dir / "triage_execution_log.json").write_text(json.dumps(execution_log, indent=2) + "\n", encoding="utf-8")

    print(f"VERIFY_PACKET")
    print(f"  total: {len(classified)}")
    print(f"  actions: {len(actions)}")
    print(f"  closed: {closed}")
    print(f"  merged: {merged}")
    print(f"  manual_review: {len(manual_review)}")
    print(f"  by_category: {by_category}")
    print(f"  report: {output_dir / 'triage_report.json'}")
    if execution_log:
        print(f"  execution_log: {output_dir / 'triage_execution_log.json'}")
    print(f"ROLLBACK_PACKET")
    print(f"  closed PRs can be reopened via GitHub UI or gh pr reopen")
    print(f"  merged PRs cannot be rolled back without revert PRs")
    print(f"QUEUE_UPDATE")
    print(f"  next: review manual_review items and re-run with --stale-days or per-repo targeting")
    print(f"APPROVAL_GATE: {'EXECUTE' if args.execute else 'DRY-RUN'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
