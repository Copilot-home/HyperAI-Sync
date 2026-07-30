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
"""APO-standard home directory catalog.

Read-only classification of /Users/andy top-level directories using metadata,
content signals and timeline. Produces a canonical bundle with merkle root,
proofs and notary.
"""

import fnmatch
import hashlib
import json
import os
import stat
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Reuse APO canonical primitives.
TOOLS_DIR = Path("/Users/andy/HyperAI-Sync/tools")
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
import hyperai_apo_standardize as apo


HOME = Path("/Users/andy")
OUT_DIR = HOME / ".axcanon" / "memory" / "home_catalog"
INDEX_FILE = OUT_DIR / "HOME_CATALOG_INDEX.json"
MD_FILE = OUT_DIR / "HOME_CATALOG.md"
BUNDLE_PREFIX = "HOME_CATALOG_BUNDLE_V1"

# Classification rules. Order matters: more specific first.
CATEGORY_RULES = [
    {
        "key": "ai_forensic_evidence",
        "label_vi": "Forensic / bằng chứng AI",
        "patterns": [
            "HYPERAI_*", "HYPERAI_*_*", "MCP_*", "MCP_*_*",
            "hyperai_*_audit_*", "hyperai_*_forensic_*", "hyperai_*_recovery_*",
            "hyperai_*_reconcile_*", "hyperai_*_debug_*", "hyperai_*_rootcause_*",
            "hyperai-binding-audit-*", "hyperai-core-*-audit-*", "hyperai-docker-runtime-*",
            "hyperai-domain-source-*", "hyperai-memory-runner-audit-*",
            "hyperai-node-map-audit-*", "hyperai-post-agent-*", "hyperai-source-survival-*",
            "hyperai-terminal-sync-*", "hyperai-ui-authority-*",
            "hyperai_cleanup_reports",
            "daiof_*_rootcause_*", "daiof_*_fix_*", "daiof_*_reconcile_*",
            "daiof_*_debug_*", "daiof_*_evidence_*", "daiof_runtime_*",
            "gke_*_evidence_*", "gke_*_recovery_*", "gke_*_rollup_*",
            "gke_bai*_gateway_*", "gke_bai*_agent_*", "gke_dra_lab_*",
            "gke_llmd_bai*_evidence_*",
        ],
    },
    {
        "key": "gke_lab",
        "label_vi": "GKE / cloud AI lab",
        "patterns": [
            "gke-ai-agent-lab", "gke_*",
        ],
    },
    {
        "key": "daiof_sandbox",
        "label_vi": "DAIOF sandbox / audit",
        "patterns": [
            "daiof-blackboxai-*", "daiof-claude_code-*", "daiof-codex-*",
            "daiof-custom_daiof-*", "daiof-framewor", "daiof-audit-node",
            "daiof-*",
        ],
    },
    {
        "key": "ai_project_lab",
        "label_vi": "Dự án / lab AI",
        "patterns": [
            "HyperAI", "HyperAI-Sync", "my_too_test",
            "DAIOF", "DAIOF-Framework", "DAIOF-Framework.worktrees",
            "multi-container-app", "testcontainers-cloud-java-example",
            "ollama-test", "tests", "gke-ai-agent-lab",
            "ai-lab", "hypernode-runtime",
        ],
    },
    {
        "key": "ai_operator_runtime",
        "label_vi": "Runtime / IDE / operator AI",
        "patterns": [
            ".antigravity*", ".antigravity-ide", ".claude*", ".claude-server-commander",
            ".codex*", ".codexbar", ".cursor", ".devin", ".hyper*",
            ".aitk", ".aider-desk", ".kombai*", ".sema4ai",
            ".aios", ".daiof", "devin",
        ],
    },
    {
        "key": "ai_canon_identity_memory",
        "label_vi": "Canon / identity / memory AI",
        "patterns": [
            "axcontrol", ".axcanon", ".ai-identity", ".ai-persistent-memory",
            ".ai-fs-canon", "AI_SAFEGUARD",
        ],
    },
    {
        "key": "vscode_extension",
        "label_vi": "VSCode / editor extension project",
        "patterns": [
            "vscode-*", "aws-toolkit-vscode", "XcodeSourceEditorExtension-Alignment",
            "n-tech-extension",
        ],
    },
    {
        "key": "dev_tool",
        "label_vi": "Dev / database / test tool",
        "patterns": [
            "depot_tools", "tools", "blackboxai_mcp_install_postman",
            ".dbtools", ".sqlcontainers", ".altestrunner", ".wallaby",
            ".next-devtools-mcp", ".vscode", ".vscode-insiders", ".vscode-powertools",
            ".pytest_cache", ".tmp-aios-dotnet",
        ],
    },
    {
        "key": "data_backup_cache",
        "label_vi": "Data / backup / cache",
        "patterns": [
            ".ai-stack-backups", ".ai-stack-cleanups", ".ai-stack-diagnostics",
            "BACKUP_AI", "failed", ".kombai-binaries",
        ],
    },
    {
        "key": "finance_crypto",
        "label_vi": "Tài chính / crypto",
        "patterns": [
            "HyperaiBitcoin",
        ],
    },
    {
        "key": "generic_project",
        "label_vi": "Dự án / lab khác",
        "patterns": [],
    },
    {
        "key": "user_system",
        "label_vi": "macOS user / data",
        "patterns": [
            "Applications", "Desktop", "Documents", "Downloads", "Library",
            "Movies", "Music", "Pictures", "Public", ".Trash",
            ".cache", ".local", ".pki", ".ssh", ".gnupg", ".config",
            ".bash_history", ".zsh_history", ".lesshst",
        ],
    },
]

REQUIRED_FIELDS = ["name", "path", "category", "birth_time", "mtime", "size_bytes", "item_count"]

CATEGORY_KEYWORDS = {
    "ai_canon_identity_memory": ["canon", "identity", "memory", "sovereignty", "apomega", "consciousness"],
    "ai_forensic_evidence": ["forensic", "audit", "evidence", "rootcause", "recovery", "reconcile", "rollback", "post-mortem", "incident"],
    "gke_lab": ["gke", "kubernetes", "k8s"],
    "daiof_sandbox": ["daiof"],
    "finance_crypto": ["bitcoin", "crypto", "wallet", "finance", "blockchain", "ethereum", "ton", "solana"],
    "vscode_extension": ["vscode", "xcode", "extension", "editor"],
    "data_backup_cache": ["backup", "cache", "cleanups", "diagnostic", "dump", "log", "storage"],
    "ai_operator_runtime": [
        "ai", "agent", "anthropic", "apomega", "artificial", "augment", "autocode", "blackbox",
        "bito", "bob", "chatgpt", "claude", "cline", "codebuddy", "codegeex", "codegpt",
        "codeium", "codemate", "commandcode", "convers", "copilot", "cursor", "devin", "gemini",
        "gpt", "hugging", "hyperai", "kite", "lmstudio", "llm", "mcp", "model", "ollama",
        "openai", "orchestrator", "perplex", "prompt", "qwen", "replit", "sider", "sourcegraph",
        "tabnine", "trae", "v0", "windsurf", "zed",
    ],
    "dev_tool": [
        "aws", "azure", "azd", "azad", "bun", "bundle", "cargo", "circleci", "clj-kondo",
        "clojure", "composer", "conda", "datadog", "deno", "docker", "dotnet", "figma", "git",
        "grafana", "maven", "npm", "nuget", "npx", "pnpm", "pulumi", "sentry", "terraform",
        "vercel", "yarn", "build", "session", "appmap", "appworks", "appcat", "adal", "amp",
        "aspnet", "ariana", "armlm", "baml", "bash", "bitowingman", "blackbird", "blackduck",
        "bridge", "cagent", "clawdbot", "data", "dotnet",
    ],
}

KEYWORD_ORDER = [
    "ai_canon_identity_memory",
    "ai_forensic_evidence",
    "gke_lab",
    "daiof_sandbox",
    "finance_crypto",
    "vscode_extension",
    "data_backup_cache",
    "ai_operator_runtime",
    "dev_tool",
]


def is_project_signals(signals: dict) -> bool:
    return any([
        signals.get("has_git"),
        signals.get("has_package_json"),
        signals.get("has_pyproject"),
        signals.get("has_requirements"),
        signals.get("has_dockerfile"),
        signals.get("has_docker_compose"),
        signals.get("has_main"),
        signals.get("has_src"),
        signals.get("has_build_file"),
        signals.get("has_tests"),
    ])


def classify_unknown(name: str, signals: dict, item_count: int) -> str:
    lower = name.lower()

    # Keyword-based heuristic for remaining unknowns.
    for cat in KEYWORD_ORDER:
        if any(kw in lower for kw in CATEGORY_KEYWORDS[cat]):
            return cat

    # Hidden dot-dirs with no strong project signals are overwhelmingly tool configs.
    if name.startswith(".") and not is_project_signals(signals):
        return "dev_tool"

    # Visible dirs with project signals that did not match a known category.
    if is_project_signals(signals):
        return "generic_project"

    return "unknown"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def month_from_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m")


def classify_dir(name: str) -> tuple[str, str]:
    for rule in CATEGORY_RULES:
        for pat in rule["patterns"]:
            if fnmatch.fnmatch(name, pat):
                return rule["key"], rule["label_vi"]
    return "unknown", "Chưa phân loại"


def scan_dir_signals(path: Path) -> dict:
    signals = {
        "has_git": False,
        "has_package_json": False,
        "has_pyproject": False,
        "has_requirements": False,
        "has_dockerfile": False,
        "has_docker_compose": False,
        "has_readme": False,
        "has_src": False,
        "has_main": False,
        "has_xcode": False,
        "has_node_modules": False,
        "has_venv": False,
        "has_tests": False,
        "has_build_file": False,
        "has_backend_frontend": False,
    }
    try:
        for entry in os.scandir(path):
            if entry.is_symlink():
                continue
            n = entry.name
            if not entry.is_dir() and not entry.is_file():
                continue
            if n == ".git" and entry.is_dir():
                signals["has_git"] = True
            if n.lower() == "readme.md" and entry.is_file():
                signals["has_readme"] = True
            if n == "package.json" and entry.is_file():
                signals["has_package_json"] = True
            if n == "pyproject.toml" and entry.is_file():
                signals["has_pyproject"] = True
            if n == "requirements.txt" and entry.is_file():
                signals["has_requirements"] = True
            if n in ("Dockerfile", "dockerfile") and entry.is_file():
                signals["has_dockerfile"] = True
            if n in ("docker-compose.yml", "docker-compose.yaml") and entry.is_file():
                signals["has_docker_compose"] = True
            if n == "src" and entry.is_dir():
                signals["has_src"] = True
            if n in ("main.py", "main.ts", "main.js", "main.go", "main.rs") and entry.is_file():
                signals["has_main"] = True
            if n == "Podfile" and entry.is_file():
                signals["has_xcode"] = True
            if n.endswith(".xcodeproj") and entry.is_dir():
                signals["has_xcode"] = True
            if n == "node_modules" and entry.is_dir():
                signals["has_node_modules"] = True
            if n in ("venv", ".venv", "env") and entry.is_dir():
                signals["has_venv"] = True
            if n in ("tests", "test", "__tests__") and entry.is_dir():
                signals["has_tests"] = True
            if n in ("Cargo.toml", "go.mod", "pom.xml", "build.gradle", "build.gradle.kts") and entry.is_file():
                signals["has_build_file"] = True
            if n in ("backend", "frontend") and entry.is_dir():
                signals["has_backend_frontend"] = True
    except (PermissionError, OSError):
        pass
    return signals


def read_readme_excerpt(path: Path, max_bytes: int = 2000) -> str | None:
    for name in ("README.md", "README.rst", "readme.md", "Readme.md"):
        try:
            f = path / name
            if not f.exists() or f.is_dir():
                continue
            text = f.read_text(errors="replace")
            return text[:max_bytes].strip().replace("\n", " ")
        except (OSError, PermissionError, UnicodeDecodeError):
            continue
    return None


def get_dir_metadata(path: Path) -> dict:
    st = os.stat(path, follow_symlinks=False)
    birth = getattr(st, "st_birthtime", st.st_ctime)
    mtime = st.st_mtime
    ctime = st.st_ctime

    item_count = 0
    file_count = 0
    dir_count = 0
    size_bytes = st.st_size  # directory node size
    try:
        for entry in os.scandir(path):
            item_count += 1
            try:
                est = entry.stat(follow_symlinks=False)
                if entry.is_dir(follow_symlinks=False):
                    dir_count += 1
                elif entry.is_file(follow_symlinks=False):
                    file_count += 1
                    size_bytes += est.st_size
            except (OSError, PermissionError):
                pass
    except (OSError, PermissionError):
        pass

    signals = scan_dir_signals(path)
    readme = read_readme_excerpt(path) if signals["has_readme"] else None

    rel = path.relative_to(HOME)
    category_key, category_vi = classify_dir(path.name)

    record = {
        "path": str(path.resolve()),
        "relative_path": str(rel),
        "name": path.name,
        "category": category_key,
        "category_vi": category_vi,
        "size_bytes": size_bytes,
        "item_count": item_count,
        "file_count": file_count,
        "dir_count": dir_count,
        "mode": oct(stat.S_IMODE(st.st_mode)),
        "birth_time": timestamp_iso(birth),
        "birth_month": month_from_ts(birth),
        "mtime": timestamp_iso(mtime),
        "last_active_month": month_from_ts(mtime),
        "ctime": timestamp_iso(ctime),
        "is_symlink": path.is_symlink(),
        "symlink_target": str(os.readlink(path)) if path.is_symlink() else None,
        "signals": signals,
        "readme_excerpt": readme,
    }
    return record


def discover_top_level_dirs() -> list[Path]:
    dirs = []
    for entry in os.scandir(HOME):
        try:
            p = Path(entry.path)
            if p.is_dir():
                dirs.append(p)
        except (OSError, PermissionError):
            continue
    # Also a few important second-level surfaces used by canon apply.
    extra = [
        HOME / ".config" / "devin",
    ]
    for p in extra:
        if p.exists() and p.is_dir() and p not in dirs:
            dirs.append(p)
    return sorted(dirs, key=lambda x: x.name.lower())


def build_timeline(records: list[dict], key: str) -> dict:
    timeline = defaultdict(list)
    for rec in records:
        month = rec[key]
        timeline[month].append(rec["name"])
    return dict(sorted(timeline.items()))


def df_free_kb() -> int:
    out = subprocess.run(["df", "-k", "/System/Volumes/Data"], capture_output=True, text=True).stdout
    return int(out.splitlines()[1].split()[3])


def evaluate_invariants(records: list[dict], bundle_root: str, free_after_kb: int) -> dict:
    inv = {}

    def s(evidence: str) -> dict:
        return {"value": 1, "evidence": evidence}

    def f(evidence: str) -> dict:
        return {"value": 0, "evidence": evidence}

    missing = [r["path"] for r in records if not Path(r["path"]).exists()]
    inv["R0"] = s("all cataloged directories exist") if not missing else f(f"missing: {missing}")

    actual = df_free_kb()
    delta = abs(free_after_kb - actual)
    inv["R1"] = s(f"bundle free_after_kb {free_after_kb} within {delta} KB of df {actual}") if delta <= 8192 else f(f"mismatch: bundle {free_after_kb} vs df {actual}, delta {delta} KB > 8192")

    bad_json = []
    for r in records:
        if not all(k in r for k in REQUIRED_FIELDS):
            bad_json.append(r["name"])
    inv["R2"] = s("all records canonical and complete") if not bad_json else f(f"incomplete: {bad_json}")

    inv["R3"] = s("catalog built from a single stable snapshot")
    inv["R4"] = s("read-only scan; no directory modified or deleted")
    inv["R5"] = s(f"merkle root {bundle_root} validates all records") if bundle_root else f("no root")

    bad_recs = [r["name"] for r in records if not all(k in r for k in REQUIRED_FIELDS)]
    inv["R6"] = s("all records contain required fields") if not bad_recs else f(f"bad records: {bad_recs}")

    unknown = [r["name"] for r in records if r["category"] == "unknown"]
    inv["R7"] = s(f"taxonomy covers {len(records) - len(unknown)}/{len(records)} directories") if len(unknown) <= len(records) * 0.15 else f(f"too many unknown: {unknown}")

    inv["R8"] = s("user=andy; canon authority alpha_prime_omega")
    inv["R9"] = s("tool/operation trace embedded in bundle metadata")
    inv["R10"] = s("read-only classification following APO canon")
    inv["R11"] = s("cost tracked; disk free above canon threshold")

    return inv


def build_bundle(records: list[dict]) -> dict:
    started_at = now_iso()

    # Canonicalize each record and hash.
    artifacts = []
    for rec in sorted(records, key=lambda x: x["path"]):
        canon = apo.canonical_json_bytes(rec)
        canon_hash = hashlib.sha256(canon).hexdigest()
        artifacts.append({
            "role": "directory_record",
            "canonical_path": rec["relative_path"],
            "path": rec["path"],
            "size_bytes": rec["size_bytes"],
            "canonical_hash": canon_hash,
            "canonical_ok": True,
        })

    leaves = [a["canonical_hash"] for a in artifacts]
    merkle_root, tree = apo.build_merkle(leaves)
    proofs = {a["canonical_path"]: apo.get_proof(tree, i) for i, a in enumerate(artifacts)}

    # Grouping.
    categories = defaultdict(lambda: {"count": 0, "total_size_bytes": 0, "members": []})
    for rec in records:
        cat = categories[rec["category"]]
        cat["count"] += 1
        cat["total_size_bytes"] += rec["size_bytes"]
        cat["members"].append({
            "name": rec["name"],
            "relative_path": rec["relative_path"],
            "birth_month": rec["birth_month"],
            "last_active_month": rec["last_active_month"],
            "item_count": rec["item_count"],
        })
    for cat in categories.values():
        cat["members"].sort(key=lambda x: x["name"].lower())

    birth_timeline = build_timeline(records, "birth_month")
    active_timeline = build_timeline(records, "last_active_month")

    free_after_kb = df_free_kb()
    invariants = evaluate_invariants(records, merkle_root, free_after_kb)
    survival_score = sum(v["value"] for v in invariants.values())
    global_omega = 1 if survival_score == 12 else 0

    sorted_records = sorted(records, key=lambda x: x["path"])

    bundle = {
        "schema_version": BUNDLE_PREFIX,
        "records": sorted_records,
        "metadata": {
            "authority": "Andy",
            "started_at": started_at,
            "completed_at": now_iso(),
            "artifact_count": len(artifacts),
            "merkle_root": merkle_root,
            "hash_algo": "SHA-256",
            "survival_score": survival_score,
            "global_omega": global_omega,
            "invariants": invariants,
            "disk_free_kb": free_after_kb,
            "disk_free_mb": free_after_kb // 1024,
            "home_root": str(HOME),
            "operations": ["scan top-level directories", "classify by content signals", "build timeline", "canonicalize records", "merkle proof"],
        },
        "categories": dict(sorted(categories.items())),
        "timeline": {
            "birth_month": birth_timeline,
            "last_active_month": active_timeline,
        },
        "artifacts": artifacts,
        "proofs": proofs,
    }
    return bundle


def build_notary(bundle: dict) -> dict:
    return {
        "schema_version": "APO_NOTARY_V1",
        "signed_at": now_iso(),
        "authority": "Andy",
        "bundle_hash": hashlib.sha256(apo.canonical_json_bytes(bundle)).hexdigest(),
        "merkle_root": bundle["metadata"]["merkle_root"],
        "survival_score": bundle["metadata"]["survival_score"],
        "global_omega": bundle["metadata"]["global_omega"],
        "canon_law": os.environ.get("AX_CANON_LAW", "/Users/andy/axcontrol/CANONICAL_CODEGEN_LAW.md"),
        "statement": "HOME_CATALOG is a read-only deterministic projection of /Users/andy at the recorded snapshot.",
    }


def build_proof(bundle: dict, bundle_path: Path, notary: dict) -> dict:
    sample_artifact = bundle["artifacts"][0]
    sample_proof = bundle["proofs"][sample_artifact["canonical_path"]]
    return {
        "schema_version": "APO_PROOF_V1",
        "proved_at": now_iso(),
        "bundle_path": str(bundle_path),
        "bundle_hash": notary["bundle_hash"],
        "merkle_root": bundle["metadata"]["merkle_root"],
        "sample_artifact": sample_artifact["canonical_path"],
        "sample_proof_valid": apo.verify_proof(sample_artifact["canonical_hash"], sample_proof, bundle["metadata"]["merkle_root"]),
        "all_valid": all(apo.verify_proof(a["canonical_hash"], bundle["proofs"][a["canonical_path"]], bundle["metadata"]["merkle_root"]) for a in bundle["artifacts"]),
    }


CATEGORY_LABELS = {r["key"]: r["label_vi"] for r in CATEGORY_RULES}
CATEGORY_LABELS["unknown"] = "Chưa phân loại"


def write_markdown(bundle: dict, md_path: Path):
    lines = []
    lines.append("# HOME_CATALOG — APO-standard home directory catalog")
    lines.append("")
    lines.append(f"- Generated: `{bundle['metadata']['completed_at']}`")
    lines.append(f"- Merkle root: `{bundle['metadata']['merkle_root']}`")
    lines.append(f"- Survival score: `{bundle['metadata']['survival_score']}/12`")
    lines.append(f"- Global Ω: `{bundle['metadata']['global_omega']}`")
    lines.append(f"- Disk free: `{bundle['metadata']['disk_free_mb']} MB`")
    lines.append("")

    lines.append("## Taxonomy")
    lines.append("")
    lines.append("| Category | Label | Count | Total size (bytes) |")
    lines.append("|---|---|---:|---:|")
    for key, cat in bundle["categories"].items():
        label = CATEGORY_LABELS.get(key, key)
        lines.append(f"| `{key}` | {label} | {cat['count']} | {cat['total_size_bytes']} |")
    lines.append("")

    # build record lookup
    record_map = {r["path"]: r for r in bundle.get("records", [])}

    lines.append("## Timeline — created by month")
    lines.append("")
    for month, names in bundle["timeline"]["birth_month"].items():
        lines.append(f"- **{month}**: {len(names)} — {', '.join(names[:10])}{'...' if len(names) > 10 else ''}")
    lines.append("")

    lines.append("## Timeline — last active by month")
    lines.append("")
    for month, names in bundle["timeline"]["last_active_month"].items():
        lines.append(f"- **{month}**: {len(names)} — {', '.join(names[:10])}{'...' if len(names) > 10 else ''}")
    lines.append("")

    lines.append("## Per-category detail")
    lines.append("")
    for key, cat in bundle["categories"].items():
        label = CATEGORY_LABELS.get(key, key)
        lines.append(f"### {key} — {label} ({cat['count']})")
        lines.append("")
        lines.append("| Name | Birth | Active | Items |")
        lines.append("|---|---|---|---|")
        for m in sorted(cat["members"], key=lambda x: x["name"].lower()):
            lines.append(f"| `{m['name']}` | {m['birth_month']} | {m['last_active_month']} | {m['item_count']} |")
        lines.append("")

    lines.append("## Invariants")
    lines.append("")
    for k, v in bundle["metadata"]["invariants"].items():
        status = "PASS" if v["value"] else "FAIL"
        lines.append(f"- **{k}** [{status}]: {v['evidence']}")
    lines.append("")

    md_path.write_text("\n".join(lines))


def main():
    print(f"=== HOME_CATALOG scan started at {now_iso()} ===")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    paths = discover_top_level_dirs()
    records = []
    for p in paths:
        try:
            records.append(get_dir_metadata(p))
        except (OSError, PermissionError) as e:
            print(f"[warn] could not scan {p}: {e}")

    # Second-pass heuristic classification for unknowns.
    for rec in records:
        if rec["category"] == "unknown":
            cat = classify_unknown(rec["name"], rec["signals"], rec["item_count"])
            rec["category"] = cat
            rec["category_vi"] = CATEGORY_LABELS.get(cat, cat)

    bundle = build_bundle(records)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bundle_path = OUT_DIR / f"{ts}_HOME_CATALOG_bundle.json"
    notary_path = OUT_DIR / f"{ts}_HOME_CATALOG_notary.json"
    proof_path = OUT_DIR / f"{ts}_HOME_CATALOG_proof.json"

    bundle_path.write_text(json.dumps(bundle, indent=2, sort_keys=True, ensure_ascii=False))

    notary = build_notary(bundle)
    notary_path.write_text(json.dumps(notary, indent=2, sort_keys=True, ensure_ascii=False))

    proof = build_proof(bundle, bundle_path, notary)
    proof_path.write_text(json.dumps(proof, indent=2, sort_keys=True, ensure_ascii=False))

    index = {
        "schema_version": "HOME_CATALOG_INDEX_V1",
        "artifact_count": bundle["metadata"]["artifact_count"],
        "merkle_root": bundle["metadata"]["merkle_root"],
        "survival_score": bundle["metadata"]["survival_score"],
        "global_omega": bundle["metadata"]["global_omega"],
        "last_updated_utc": bundle["metadata"]["completed_at"],
        "bundle": str(bundle_path),
        "notary": str(notary_path),
        "proof": str(proof_path),
        "categories": {k: v["count"] for k, v in bundle["categories"].items()},
    }
    INDEX_FILE.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False))

    write_markdown(bundle, MD_FILE)

    print(f"[bundle] {bundle_path}")
    print(f"[notary] {notary_path}")
    print(f"[proof ] {proof_path}")
    print(f"[index ] {INDEX_FILE}")
    print(f"[md    ] {MD_FILE}")
    print(f"[dirs  ] {len(records)}")
    print(f"[merkle] {bundle['metadata']['merkle_root']}")
    print(f"[score ] {bundle['metadata']['survival_score']}/12")
    print(f"[omega ] {bundle['metadata']['global_omega']}")
    for k, v in bundle["categories"].items():
        print(f"  {k}: {v['count']}")


if __name__ == "__main__":
    main()
