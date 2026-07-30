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
"""NotebookLM Mode C portable bundle compiler for Σ_APΩ.

Produces a stable set of source documents, a knowledge graph across four planes,
and a causal context index from local canon + runtime evidence. Default is
portable manual upload (Mode C). Mode A Google-Drive sync requires explicit
credentials and the `--drive-sync` flag; Mode B Enterprise API is not implemented.

The hub recompiles this bundle on every patrol cycle by calling `compile()`.
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

sys.path.insert(0, str(Path(__file__).resolve().parents[0]))
import hyperai_notebooklm_mindmap as mindmap
import hyperai_notebooklm_drive as drive
import hyperai_notebooklm_query as query


HOME = Path("/Users/andy")
CANON_ROOT = HOME / "axcontrol"
HYPERAI_ROOT = HOME / "HyperAI-Sync"
MEMORY = HOME / ".axcanon" / "memory"
OUT = MEMORY / "notebooklm"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any | None = None) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_text_or_default(path: Path, default: str = "") -> str:
    if not path.exists():
        return default
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return default


SOURCE_SPECS: list[dict[str, Any]] = [
    {
        "id": "NB-S01",
        "plane": "knowledge",
        "title": "Σ_APΩ Operational Axioms",
        "out_name": "01_knowledge_axioms.md",
        "source_paths": [CANON_ROOT / "docs" / "Sigma_APO_Operational_Canon.md"],
    },
    {
        "id": "NB-S02",
        "plane": "knowledge",
        "title": "Σ_APΩ System Documentation",
        "out_name": "02_knowledge_system.md",
        "source_paths": [HYPERAI_ROOT / "memory" / "Sigma_APO_Complete_System_Documentation.md"],
    },
    {
        "id": "NB-S03",
        "plane": "connectors",
        "title": "APΩ Credential & Secret Sync",
        "out_name": "03_connectors_credentials.md",
        "source_paths": [
            HYPERAI_ROOT / "memory" / "APΩ_CREDENTIAL_CANON.md",
            HYPERAI_ROOT / "vscode-secret-sync" / "README.md",
        ],
    },
    {
        "id": "NB-S04",
        "plane": "execution",
        "title": "Σ_APΩ Sleep & Night Watch",
        "out_name": "04_execution_sleep.md",
        "source_paths": [CANON_ROOT / "docs" / "Sigma_APO_Sleep_Workflow.md"],
    },
    {
        "id": "NB-S05",
        "plane": "execution",
        "title": "Agent Capsules & Runtime State",
        "out_name": "05_execution_runtime.md",
        "source_paths": [
            HYPERAI_ROOT / "memory" / "agent6_synthesis_capsule.md",
            HYPERAI_ROOT / "memory" / "HAIOS_STATE_MODEL.md",
        ],
    },
]


def compile_evidence_document() -> str:
    """Build 06_evidence_state.md from the latest runtime artifacts."""
    sigma_verify = load_json(MEMORY / "SIGMA_APO_VERIFY.json", {})
    secret_verify = load_json(MEMORY / "secrets" / "SECRETS_SYNC_VERIFY.json", {})
    night_watch = load_json(MEMORY / "night_watch_summary.json", {})
    apo_index = load_json(
        HYPERAI_ROOT / "runtime" / "federation_orchestrator" / "cleanup_receipts" / "APO_cleanup_index.json",
        {},
    )
    home_index = load_json(MEMORY / "home_catalog" / "HOME_CATALOG_INDEX.json", {})
    secrets_index = load_json(MEMORY / "secrets" / "SECRETS_SYNC_INDEX.json", {})

    sigma = sigma_verify.get("surfaces", {})
    secret = secret_verify.get("surfaces", {})
    apo = {
        "artifacts": apo_index.get("artifact_count", 0),
        "omega": apo_index.get("global_omega"),
        "merkle_root": apo_index.get("merkle_root", "")[:16] + "...",
    }
    home = {
        "directories": home_index.get("artifact_count", 0),
        "categories": len(home_index.get("categories", {})),
        "merkle_root": home_index.get("merkle_root", "")[:16] + "...",
    }
    secrets = {
        "surfaces": secrets_index.get("totals", {}).get("total_surfaces", 0),
        "omega": secrets_index.get("global_omega"),
    }
    watch = {
        "last": night_watch.get("at", "never"),
        "omega": night_watch.get("omega"),
        "asleep": night_watch.get("asleep"),
    }

    sections = [
        "# Current Runtime Evidence",
        "",
        f"- generated: {now_iso()}",
        "- plane: evidence",
        "- identity: NB-S06",
        "",
        "## Σ_APΩ Surface Verification",
        "",
        f"- total surfaces: {sigma.get('total', 0)}",
        f"- anchored OK: {sigma.get('ok', 0)}",
        f"- env file: {sigma_verify.get('env_file', {}).get('all_present', False)}",
        f"- launchctl: {sigma_verify.get('launchctl', {}).get('ok', False)}",
        f"- APO artifacts: {apo['artifacts']}",
        f"- APO Ω: {apo['omega']}",
        f"- APO merkle: {apo['merkle_root']}",
        "",
        "## SecretStorage Sync",
        "",
        f"- total surfaces: {secret.get('total', 0)}",
        f"- fully anchored: {secret.get('ok', 0)}",
        f"- Python round-trip: {secret_verify.get('python_test', {}).get('get_ok', False)}",
        f"- TypeScript round-trip: {secret_verify.get('typescript_test', {}).get('get_ok', False)}",
        f"- Cross-sync: {secret_verify.get('cross_sync_test', {}).get('ts_get_ok', False)}",
        f"- SECRETS_SYNC Ω: {secrets.get('omega')}",
        f"- SECRETS_SYNC surfaces: {secrets.get('surfaces', 0)}",
        "",
        "## Night Watch",
        "",
        f"- last patrol: {watch['last']}",
        f"- sleep mode: {watch.get('asleep', False)}",
        f"- patrol Ω: {watch.get('omega')}",
        "",
        "## Home Catalog",
        "",
        f"- directories: {home.get('directories')}",
        f"- categories: {home.get('categories')}",
        f"- merkle: {home.get('merkle_root')}",
        "",
        "## Raw paths",
        "",
        f"- SIGMA_APO_VERIFY: {MEMORY / 'SIGMA_APO_VERIFY.json'}",
        f"- SECRETS_SYNC_VERIFY: {MEMORY / 'secrets' / 'SECRETS_SYNC_VERIFY.json'}",
        f"- APO_cleanup_index: {HYPERAI_ROOT / 'runtime' / 'federation_orchestrator' / 'cleanup_receipts' / 'APO_cleanup_index.json'}",
        f"- HOME_CATALOG: {MEMORY / 'home_catalog' / 'HOME_CATALOG.md'}",
    ]
    return "\n".join(sections)


def compile_source(spec: dict[str, Any]) -> str:
    """Compile one bounded source document from its source paths."""
    body_parts: list[str] = []
    for src in spec["source_paths"]:
        if isinstance(src, Path):
            body_parts.append(read_text_or_default(src, f"<!-- missing: {src} -->"))
        else:
            body_parts.append(str(src))
    body = "\n\n---\n\n".join(body_parts)

    frontmatter = [
        f"# {spec['title']}",
        "",
        f"- identity: {spec['id']}",
        f"- plane: {spec['plane']}",
        f"- generated: {now_iso()}",
        f"- out_name: {spec['out_name']}",
    ]
    if spec.get("source_paths"):
        frontmatter.append("- sources:")
        for src in spec["source_paths"]:
            frontmatter.append(f"  - {src}")
    frontmatter.append("")
    return "\n".join(frontmatter) + body


def build_knowledge_graph(sources: list[dict[str, Any]]) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []

    concept_nodes = [
        {"id": "omega_axiom", "label": "Ω axiom", "plane": "knowledge", "source_doc": "NB-S01"},
        {"id": "thirteen_layers", "label": "13 layers", "plane": "knowledge", "source_doc": "NB-S01"},
        {"id": "fifteen_modules", "label": "15 Creator Modules", "plane": "knowledge", "source_doc": "NB-S01"},
        {"id": "d_trajectory", "label": "D trajectory", "plane": "knowledge", "source_doc": "NB-S01"},
        {"id": "ab_proof", "label": "AB Proof", "plane": "knowledge", "source_doc": "NB-S01"},
        {"id": "wfq", "label": "WFQ fairness", "plane": "knowledge", "source_doc": "NB-S01"},
        {"id": "backend", "label": "Production Backend", "plane": "knowledge", "source_doc": "NB-S02"},
        {"id": "dashboard", "label": "Dashboard", "plane": "knowledge", "source_doc": "NB-S02"},
        {"id": "file_tree", "label": "87+ file tree", "plane": "knowledge", "source_doc": "NB-S02"},
        {"id": "credential_canon", "label": "Credential Canon", "plane": "connectors", "source_doc": "NB-S03"},
        {"id": "secret_vault", "label": "APO Secret Vault", "plane": "connectors", "source_doc": "NB-S03"},
        {"id": "secret_sync", "label": "VS Code SecretStorage Sync", "plane": "connectors", "source_doc": "NB-S03"},
        {"id": "night_watch", "label": "Night Watch", "plane": "execution", "source_doc": "NB-S04"},
        {"id": "launchd", "label": "launchd scheduler", "plane": "execution", "source_doc": "NB-S04"},
        {"id": "agent_loop", "label": "Agent Capsules & OODA", "plane": "execution", "source_doc": "NB-S05"},
        {"id": "runtime_state", "label": "Runtime State", "plane": "execution", "source_doc": "NB-S05"},
        {"id": "sigma_verify", "label": "Σ_APΩ Surface Verify", "plane": "evidence", "source_doc": "NB-S06"},
        {"id": "secret_verify", "label": "SecretStorage Sync Verify", "plane": "evidence", "source_doc": "NB-S06"},
        {"id": "apo_bundle", "label": "APO Bundle", "plane": "evidence", "source_doc": "NB-S06"},
        {"id": "home_catalog", "label": "HOME_CATALOG", "plane": "evidence", "source_doc": "NB-S06"},
    ]

    for spec in sources:
        nodes.append({
            "id": spec["id"],
            "label": spec["title"],
            "plane": spec["plane"],
            "type": "source_document",
            "path": spec["out_name"],
        })

    nodes.extend(concept_nodes)

    edge_defs = [
        ("omega_axiom", "thirteen_layers", "defines"),
        ("omega_axiom", "fifteen_modules", "defines"),
        ("omega_axiom", "d_trajectory", "defines"),
        ("thirteen_layers", "backend", "realized_by"),
        ("fifteen_modules", "ab_proof", "includes"),
        ("fifteen_modules", "wfq", "includes"),
        ("backend", "dashboard", "observed_by"),
        ("backend", "file_tree", "implemented_by"),
        ("credential_canon", "secret_vault", "governs"),
        ("secret_vault", "secret_sync", "implemented_by"),
        ("secret_sync", "backend", "feeds"),
        ("ab_proof", "night_watch", "enforces"),
        ("wfq", "night_watch", "enforces"),
        ("night_watch", "launchd", "scheduled_by"),
        ("night_watch", "sigma_verify", "runs"),
        ("night_watch", "secret_verify", "runs"),
        ("agent_loop", "night_watch", "coordinates"),
        ("runtime_state", "agent_loop", "reported_by"),
        ("sigma_verify", "apo_bundle", "validates"),
        ("secret_verify", "secret_vault", "validates"),
        ("home_catalog", "sigma_verify", "enumerated_by"),
        ("apo_bundle", "NB-S06", "produces"),
    ]
    for src, dst, rel in edge_defs:
        edges.append({"from": src, "to": dst, "relation": rel})

    return {
        "schema_version": "NOTEBOOKLM_KG_V1",
        "generated_at": now_iso(),
        "planes": {
            "knowledge": [n for n in nodes if n["plane"] == "knowledge"],
            "execution": [n for n in nodes if n["plane"] == "execution"],
            "connectors": [n for n in nodes if n["plane"] == "connectors"],
            "evidence": [n for n in nodes if n["plane"] == "evidence"],
        },
        "edges": edges,
    }


def build_context_index(sources: list[dict[str, Any]]) -> str:
    lines = [
        "# NotebookLM Context Index",
        "",
        f"- generated: {now_iso()}",
        "- role: causal spine for source-grounded exploration",
        "- flow: Observe → Diagnose → Plan → Approval Gate → Execute → Verify → Record",
        "",
        "## 1. Observe",
        "",
        "- Read the runtime evidence plane.",
        "- Source: `06_evidence_state.md` (NB-S06)",
        "- Inputs: SIGMA_APO_VERIFY, SECRETS_SYNC_VERIFY, night_watch_summary, APO_cleanup_index, HOME_CATALOG.",
        "",
        "## 2. Diagnose",
        "",
        "- Use the Ω axiom, 13 layers, and 15 modules to classify drift.",
        "- Sources: `01_knowledge_axioms.md` (NB-S01)",
        "",
        "## 3. Plan",
        "",
        "- Map remediation to execution plane: night watch schedules, agent loops, cleanup dry-runs.",
        "- Sources: `04_execution_sleep.md` (NB-S04), `05_execution_runtime.md` (NB-S05)",
        "",
        "## 4. Approval Gate",
        "",
        "- All destructive or external actions require explicit gate.",
        "- Credential/connector plane defines secret ownership and keychain fallback.",
        "- Source: `03_connectors_credentials.md` (NB-S03)",
        "",
        "## 5. Execute",
        "",
        "- Run the chosen action through the appropriate runtime (local script, launchd, or approved cloud call).",
        "- Sources: `04_execution_sleep.md` (NB-S04), `05_execution_runtime.md` (NB-S05)",
        "",
        "## 6. Verify",
        "",
        "- Run SIGMA_APO_VERIFY and SECRETS_SYNC_VERIFY.",
        "- Check APO_cleanup_index Ω and survival score.",
        "- Source: `06_evidence_state.md` (NB-S06)",
        "",
        "## 7. Record",
        "",
        "- Write receipts, notary, proof, and update `brain.index`.",
        "- Recompile NotebookLM bundle for the next read cycle.",
        "- Source: `06_evidence_state.md` (NB-S06), `02_knowledge_system.md` (NB-S02)",
        "",
        "## Source documents",
        "",
    ]
    for spec in sources:
        lines.append(f"- `{spec['out_name']}` | {spec['id']} | plane={spec['plane']} | {spec['title']}")
    lines.extend([
        "",
        "## Knowledge graph",
        "",
        "- `knowledge_graph.json` organizes four planes: knowledge, execution, connectors, evidence.",
        "- The graph is data, not a second visual editor.",
    ])
    return "\n".join(lines)


def compile(bundle_dir: Path | None = None, mode: str = "c") -> dict[str, Any]:
    out = bundle_dir or OUT
    out.mkdir(parents=True, mode=0o700, exist_ok=True)

    sources = list(SOURCE_SPECS)
    sources.append({
        "id": "NB-S06",
        "plane": "evidence",
        "title": "Current Runtime Evidence",
        "out_name": "06_evidence_state.md",
        "source_paths": [],
        "generated": True,
    })

    written: list[str] = []
    for spec in sources:
        if spec.get("generated"):
            content = compile_evidence_document()
        else:
            content = compile_source(spec)
        path = out / spec["out_name"]
        path.write_text(content, encoding="utf-8")
        written.append(str(path))

    graph = build_knowledge_graph(sources)
    graph_path = out / "knowledge_graph.json"
    graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    mindmap_path = out / "mindmap.md"
    flowchart_path = out / "flowchart.md"
    mindmap_path.write_text(mindmap.make_mindmap(graph), encoding="utf-8")
    flowchart_path.write_text(mindmap.make_flowchart(graph), encoding="utf-8")

    context = build_context_index(sources)
    context_path = out / "context_index.md"
    context_path.write_text(context, encoding="utf-8")

    synthesis_path = None
    synthesis_error = None
    try:
        synthesis_path = query.synthesize(model=os.environ.get("AX_NOTEBOOKLM_SYNTH_MODEL", "qwen2.5:1.5b"))
    except Exception as e:
        synthesis_error = str(e)

    manifest = {
        "schema_version": "NOTEBOOKLM_BUNDLE_V1",
        "generated_at": now_iso(),
        "mode": mode,
        "directory": str(out),
        "source_documents": [
            {"id": s["id"], "title": s["title"], "plane": s["plane"], "path": s["out_name"]}
            for s in sources
        ],
        "knowledge_graph": str(graph_path),
        "mindmap": str(mindmap_path),
        "flowchart": str(flowchart_path),
        "synthesis": str(synthesis_path) if synthesis_path else None,
        "context_index": str(context_path),
        "instructions": "Upload the six source_documents, context_index.md, and optionally knowledge_graph.json into one NotebookLM notebook. mindmap.md and flowchart.md are local Mermaid renderings. synthesis.md is a model-generated structured read summary.",
    }

    manifest_path = out / "notebooklm_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    result = {
        "mode": mode,
        "directory": str(out),
        "source_documents": [s["out_name"] for s in sources],
        "graph": str(graph_path),
        "mindmap": str(mindmap_path),
        "flowchart": str(flowchart_path),
        "context": str(context_path),
        "manifest": str(manifest_path),
    }
    if synthesis_path:
        result["synthesis"] = str(synthesis_path)
    if synthesis_error:
        result["synthesis_error"] = synthesis_error
    return result


def run_consumer_sync() -> dict[str, Any]:
    consumer = Path(__file__).resolve().parent / "hyperai_notebooklm_consumer.py"
    try:
        proc = subprocess.run(
            [sys.executable, str(consumer)],
            capture_output=True,
            text=True,
            timeout=600,
            check=True,
        )
        return json.loads(proc.stdout)
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile NotebookLM portable bundle")
    parser.add_argument("--out", type=Path, default=OUT, help="Output directory")
    parser.add_argument("--mode", choices=["a", "b", "c"], default="c", help="Mode: a=Drive, b=API, c=portable")
    parser.add_argument("--drive-sync", action="store_true", help="Sync the compiled bundle to Google Drive as 6 Google Docs (Mode A)")
    parser.add_argument("--consumer-sync", action="store_true", help="Drive consumer NotebookLM via notebooklm-py: create notebook, add sources, generate mind map (Mode C)")
    args = parser.parse_args()

    if args.drive_sync:
        if not os.environ.get("AX_NOTEBOOKLM_DRIVE_ENABLED"):
            print("[error] Mode A sync requires AX_NOTEBOOKLM_DRIVE_ENABLED and gcloud Drive scope.", file=os.sys.stderr)
            return 1

    if args.consumer_sync:
        if not os.environ.get("AX_NOTEBOOKLM_CONSUMER_ENABLED"):
            print("[error] Mode C consumer sync requires AX_NOTEBOOKLM_CONSUMER_ENABLED=1.", file=os.sys.stderr)
            return 1

    summary = compile(bundle_dir=args.out, mode=args.mode)

    if args.drive_sync:
        try:
            drive_summary = drive.sync(force=True)
            summary["drive_sync"] = drive_summary
        except Exception as e:
            print(f"[error] Drive sync failed: {e}", file=os.sys.stderr)
            return 1

    if args.consumer_sync:
        summary["consumer_sync"] = run_consumer_sync()

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
