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

"""HyperAI repository governance agent.

Scans all repositories under configured owners, triages open issues and PRs,
optionally performs low-risk cleanup, and reconciles Notion-sync issues with
Notion source status.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime" / "federation_orchestrator"
EVIDENCE_DIR = RUNTIME / "agent_task_outputs"

DEFAULT_OWNERS = ["NguyenCuong1989", "Copilot-home", "LineageAI"]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_gh(args: list[str]) -> dict | list:
    cmd = ["gh"] + args
    env = os.environ.copy()
    for key in ("GITHUB_TOKEN", "GH_TOKEN"):
        env.pop(key, None)
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        print(f"gh failed: {result.stderr}", file=sys.stderr)
        return []
    return json.loads(result.stdout) if result.stdout.strip() else []


def get_owner_repos(owner: str) -> list[str]:
    """List non-archived repos under an owner, sorted by recent push."""
    repos = run_gh(["search", "repos", "--owner", owner, "--archived=false", "--sort", "updated", "--order", "desc", "--limit", "1000", "--json", "fullName,openIssuesCount"])
    return [r["fullName"] for r in repos if r.get("openIssuesCount", 0) > 0 or r.get("openIssuesCount") is None]


def get_repo_issues(repo: str) -> list[dict[str, Any]]:
    """Fetch open issues for a single repo via REST; filters out pull requests."""
    raw = run_gh(["api", f"repos/{repo}/issues?state=open&per_page=100"])
    issues: list[dict[str, Any]] = []
    for item in raw:
        if "pull_request" in item:
            continue
        issues.append({
            "repository": {"nameWithOwner": repo},
            "number": item["number"],
            "title": item["title"],
            "body": item.get("body") or "",
            "createdAt": item["created_at"],
            "updatedAt": item["updated_at"],
            "commentsCount": item.get("comments", 0),
            "labels": [{"name": label.get("name", "")} for label in item.get("labels", [])],
        })
    return issues


def get_owner_issues(owner: str) -> list[dict[str, Any]]:
    """Fetch open issues for all repos under an owner; robust for orgs where search indexing is delayed."""
    repos = get_owner_repos(owner)
    all_issues: list[dict[str, Any]] = []
    for repo in repos:
        all_issues.extend(get_repo_issues(repo))
    return all_issues


def strip_uuid_dashes(page_id: str) -> str:
    return page_id.replace("-", "")


def get_notion_id_from_url(url: str) -> str:
    """Extract the undashed page id from a Notion URL like https://app.notion.com/<id>."""
    m = re.search(r"/([0-9a-f]{32})$", url)
    return m.group(1) if m else ""


def get_notion_page_map(notion_status_file: Path | None) -> dict[str, dict[str, Any]] | None:
    """Load a map of Notion page id (undashed) -> {Task Name, Status}."""
    if not notion_status_file:
        return None
    text = notion_status_file.read_text(encoding="utf-8")
    # The file may be raw JSON from the MCP query, possibly with a leading object wrapper.
    data = json.loads(text)
    if isinstance(data, dict) and "results" in data:
        rows = data["results"]
    elif isinstance(data, list):
        rows = data
    else:
        rows = data.get("results", [])
    page_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        url = row.get("url", "")
        page_id = get_notion_id_from_url(url)
        if page_id:
            page_map[page_id] = row
    return page_map


def _notion_page_url(page_id: str) -> str:
    """Build a canonical Notion page URL from a (possibly dashed) page id."""
    return f"https://app.notion.com/{strip_uuid_dashes(page_id)}"


def query_notion_database(db_id: str) -> dict[str, dict[str, Any]] | None:
    """Query a Notion database directly using NOTION_API_KEY from environment.

    Never log the token. Returns a map of page id (undashed) -> {Task Name, Status}.
    """
    token = os.environ.get("NOTION_API_KEY")
    if not token:
        print("NOTION_API_KEY not set; cannot query Notion directly.", file=sys.stderr)
        return None
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    rows: list[dict[str, Any]] = []
    next_cursor: str | None = None
    while True:
        payload = json.dumps({"start_cursor": next_cursor} if next_cursor else {})
        req = urllib.request.Request(
            url, data=payload.encode("utf-8"), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            print(f"Notion query failed: {e.code} {e.reason}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Notion query error: {e}", file=sys.stderr)
            return None
        for page in data.get("results", []):
            props = page.get("properties", {})
            status = ""
            if "Status" in props:
                status = props["Status"].get("status", {}).get("name", "")
            task_name = ""
            if "Task Name" in props:
                title = props["Task Name"].get("title", [])
                task_name = "".join(t.get("plain_text", "") for t in title)
            rows.append(
                {
                    "url": _notion_page_url(page.get("id", "")),
                    "Task Name": task_name,
                    "Status": status,
                }
            )
        next_cursor = data.get("next_cursor")
        if not next_cursor:
            break
    page_map: dict[str, dict[str, Any]] = {}
    for row in rows:
        pid = get_notion_id_from_url(row["url"])
        if pid:
            page_map[pid] = row
    return page_map


def extract_notion_page_id(body: str) -> str | None:
    m = re.search(r"Notion Page ID:\s*([0-9a-fA-F\-]{32,36})", body)
    return m.group(1) if m else None


def classify_issue(issue: dict[str, Any], page_map: dict[str, dict[str, Any]] | None, stale_days: int) -> str:
    labels = {l.get("name", "") for l in issue.get("labels", [])}
    title = issue.get("title", "")
    body = issue.get("body") or ""

    if "notion-sync" in labels:
        page_id = extract_notion_page_id(body)
        if page_id and page_map:
            undashed = strip_uuid_dashes(page_id)
            row = page_map.get(undashed)
            if not row:
                return "notion_missing"
            status = (row.get("Status") or "").lower()
            if status == "done":
                return "notion_done"
            if status == "in progress":
                return "notion_in_progress"
            return "notion_open"
        return "notion_unverified"

    if not title.strip() or title.lower().startswith(("test", "draft")) or not body.strip():
        return "junk"

    updated = issue.get("updatedAt")
    if updated:
        try:
            last_update = datetime.fromisoformat(updated.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - last_update).days
            if age_days > stale_days and issue.get("commentsCount", 0) == 0:
                return "stale"
        except Exception:
            pass

    return "manual_review"


def close_issue(repo: str, number: int, reason: str, execute: bool) -> dict[str, Any]:
    action = {"repo": repo, "number": number, "reason": reason, "closed": False}
    if execute:
        comment = f"Closed by HyperAI repo governance: {reason}\n\nGenerated with [Devin](https://devin.ai)"
        env = os.environ.copy()
        for key in ("GITHUB_TOKEN", "GH_TOKEN"):
            env.pop(key, None)
        result = subprocess.run(
            ["gh", "issue", "close", str(number), "--repo", repo, "--comment", comment],
            capture_output=True, text=True, env=env,
        )
        action["closed"] = result.returncode == 0
        if result.returncode != 0:
            print(f"  close failed for {repo}#{number}: {result.stderr.strip()}", file=sys.stderr)
    return action


def main() -> int:
    parser = argparse.ArgumentParser(description="HyperAI repository governance agent")
    parser.add_argument("--owners", nargs="+", default=DEFAULT_OWNERS)
    parser.add_argument("--stale-days", type=int, default=90)
    parser.add_argument("--notion-status-file", type=Path, default=None)
    parser.add_argument("--notion-db-id", default=None, help="Notion database id to query directly via NOTION_API_KEY")
    parser.add_argument("--execute", action="store_true", help="perform low-risk actions")
    parser.add_argument("--mission-id", default=f"mission-repo-governance-{now_iso()[:10].replace('-', '')}")
    args = parser.parse_args()

    mission_dir = EVIDENCE_DIR / args.mission_id
    mission_dir.mkdir(parents=True, exist_ok=True)

    page_map = get_notion_page_map(args.notion_status_file)
    if not page_map and args.notion_db_id:
        page_map = query_notion_database(args.notion_db_id)
        if page_map:
            print(f"Queried Notion DB {args.notion_db_id}: {len(page_map)} pages")

    all_issues: list[dict[str, Any]] = []
    for owner in args.owners:
        issues = get_owner_issues(owner)
        all_issues.extend(issues)

    # Build report
    report: dict[str, Any] = {
        "mission_id": args.mission_id,
        "timestamp": now_iso(),
        "owners": args.owners,
        "stale_days": args.stale_days,
        "notion_status_file": str(args.notion_status_file) if args.notion_status_file else None,
        "notion_db_id": args.notion_db_id,
        "total_open_issues": len(all_issues),
        "by_category": {},
        "actions": [],
        "manual_review": [],
    }

    category_counts: dict[str, int] = {}
    for issue in all_issues:
        category = classify_issue(issue, page_map, args.stale_days)
        category_counts[category] = category_counts.get(category, 0) + 1
        repo = issue["repository"]["nameWithOwner"]
        number = issue["number"]

        if category in ("notion_done", "notion_missing", "junk", "stale"):
            reason_map = {
                "notion_done": "Notion source status is Done",
                "notion_missing": "Notion source page no longer found",
                "junk": "junk/empty issue",
                "stale": f"no activity for > {args.stale_days} days",
            }
            action = close_issue(repo, number, reason_map[category], args.execute)
            report["actions"].append({
                **action,
                "title": issue.get("title"),
                "category": category,
            })
        elif category in ("notion_open", "notion_in_progress", "notion_unverified", "manual_review"):
            report["manual_review"].append({
                "repo": repo,
                "number": number,
                "title": issue.get("title"),
                "category": category,
            })

    report["by_category"] = category_counts

    report_path = mission_dir / "governance_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Report: {report_path}")
    print(f"Total open issues: {len(all_issues)}")
    print(f"Categories: {category_counts}")
    print(f"Actions: {len(report['actions'])}")
    print(f"Manual review: {len(report['manual_review'])}")

    if not args.execute:
        print("Dry-run complete. Add --execute to close issues.")

    return 0


if __name__ == "__main__":
    sys.exit(main())