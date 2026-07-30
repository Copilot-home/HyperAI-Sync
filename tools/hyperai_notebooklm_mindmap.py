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
"""Render a Mermaid mind map from the NotebookLM knowledge graph.

This is a derived view, not the source of truth. The graph data remains in
`knowledge_graph.json`. The mind map is generated for local preview or upload
into any Mermaid renderer.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


BUNDLE = Path("/Users/andy/.axcanon/memory/notebooklm")
GRAPH = BUNDLE / "knowledge_graph.json"
OUT = BUNDLE / "mindmap.md"


def load_graph() -> dict[str, Any]:
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def make_mindmap(graph: dict[str, Any]) -> str:
    lines = [
        "# Σ_APΩ Mind Map",
        "",
        "Derived from `knowledge_graph.json`.",
        "",
        "```mermaid",
        "mindmap",
        '  root((Σ_APΩ))',
    ]

    planes = graph.get("planes", {})
    for plane in ("knowledge", "execution", "connectors", "evidence"):
        nodes = planes.get(plane, [])
        if not nodes:
            continue

        label = f"{plane.upper()} plane"
        lines.append(f"    {plane}({label})")

        source_docs = [n for n in nodes if n.get("type") == "source_document"]
        concepts = [n for n in nodes if n.get("type") != "source_document"]

        for s in source_docs:
            safe_id = s["id"].replace("-", "_")
            title = s["label"].replace('"', "'")
            lines.append(f"      {safe_id}[{title}]")

        for c in concepts:
            safe_id = c["id"].replace("-", "_")
            label = c["label"].replace('"', "'")
            lines.append(f"      {safe_id}({label})")

    lines.append("```")
    return "\n".join(lines)


def make_flowchart(graph: dict[str, Any]) -> str:
    """Optional: a flowchart rendering of the knowledge graph edges."""
    lines = [
        "# Σ_APΩ Knowledge Graph Flowchart",
        "",
        "```mermaid",
        "graph LR",
    ]
    seen_ids: set[str] = set()
    for plane, nodes in graph.get("planes", {}).items():
        for n in nodes:
            sid = n["id"].replace("-", "_")
            if sid in seen_ids:
                continue
            seen_ids.add(sid)
            label = n["label"].replace('"', "'")
            if n.get("type") == "source_document":
                lines.append(f'    {sid}["{label}"]')
            else:
                lines.append(f'    {sid}(("{label}"))')
    for e in graph.get("edges", []):
        src = e["from"].replace("-", "_")
        dst = e["to"].replace("-", "_")
        rel = e.get("relation", "rel").replace('"', "'")
        lines.append(f'    {src} -->|{rel}| {dst}')
    lines.append("```")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Mermaid mind map from knowledge graph")
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--flowchart", action="store_true", help="Also write flowchart.md")
    args = parser.parse_args()

    graph = load_graph()
    mindmap = make_mindmap(graph)
    args.out.write_text(mindmap, encoding="utf-8")

    if args.flowchart:
        flow_path = args.out.parent / "flowchart.md"
        flow_path.write_text(make_flowchart(graph), encoding="utf-8")

    print(f"mindmap written: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
