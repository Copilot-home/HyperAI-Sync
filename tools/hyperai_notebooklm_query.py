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
"""Source-grounded NotebookLM-style query over the Σ_APΩ portable bundle.

Answers are generated from the six bounded source documents, context_index,
and knowledge_graph. No external search is used; the model only consumes the
local APO/Σ_APΩ corpus.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


BUNDLE = Path("/Users/andy/.axcanon/memory/notebooklm")
MANIFEST = BUNDLE / "notebooklm_manifest.json"
CONTEXT = BUNDLE / "context_index.md"
GRAPH = BUNDLE / "knowledge_graph.json"


def load_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def load_sources() -> list[dict[str, Any]]:
    if not MANIFEST.exists():
        return []
    manifest = json.loads(MANIFEST.read_text())
    sources = []
    for src in manifest.get("source_documents", []):
        path = BUNDLE / src["path"]
        text = load_text(path)
        sources.append(
            {
                "id": src["id"],
                "title": src["title"],
                "plane": src["plane"],
                "path": str(path),
                "text": text,
            }
        )
    return sources


def score_relevance(sources: list[dict[str, Any]], question: str) -> list[tuple[int, dict[str, Any]]]:
    """Crude but deterministic keyword scoring."""
    q = question.lower()
    scores = []
    for s in sources:
        score = 0
        text = s["text"].lower()
        # Whole word / phrase hits.
        for word in re.findall(r"\w+", q):
            if word in text:
                score += text.count(word)
        # Plane boost.
        if "ngủ" in q or "sleep" in q or "night watch" in q:
            if s["plane"] == "execution" and "sleep" in text:
                score += 50
        if "ω" in q or "omega" in q or "axiom" in q or "13 lớp" in q:
            if s["plane"] == "knowledge":
                score += 50
        if "secret" in q or "credential" in q or "vault" in q:
            if s["plane"] == "connectors":
                score += 50
        if "verify" in q or "chứng" in q or "evidence" in q:
            if s["plane"] == "evidence":
                score += 50
        scores.append((score, s))
    scores.sort(key=lambda x: x[0], reverse=True)
    return scores


def build_context(question: str, top_k: int = 4) -> str:
    sources = load_sources()
    ranked = score_relevance(sources, question)
    selected = [s for _, s in ranked[:top_k]]

    # Always include context index.
    ctx = f"# Context Index\n\n{load_text(CONTEXT)}\n\n---\n\n"

    for s in selected:
        ctx += f"# Source {s['id']}: {s['title']} (plane={s['plane']})\n\n{s['text']}\n\n---\n\n"
    return ctx


def ollama_generate(prompt: str, model: str = "qwen2.5:1.5b", timeout: int = 180) -> str:
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": 0.3}})
    try:
        import urllib.request
        req = urllib.request.Request(f"{host}/api/generate", data=payload.encode(), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "")
    except Exception as e:
        return f"[ollama error] {e}"


def build_prompt(context: str, question: str) -> str:
    return (
        "Bạn là NotebookLM — một mô hình đọc ngữ nghĩa (semantic read model). "
        "Chỉ sử dụng các tài liệu nguồn bên dưới để trả lời. "
        "Không dùng kiến thức bên ngoài. "
        "Trích dẫn nguồn bằng [NB-Sxx: tiêu đề tài liệu]. "
        "Trả lời ngắn gọn, rõ ràng, theo cấu trúc: Toán học / Ví dụ thực tế / Kết luận.\n\n"
        "--- TÀI LIỆU NGUỒN ---\n\n"
        f"{context}\n\n"
        "--- CÂU HỎI ---\n\n"
        f"{question}\n\n"
        "--- TRẢ LỜI ---\n"
    )


def build_full_context() -> str:
    """Load all 6 source docs, context index, and knowledge graph for synthesis."""
    sources = load_sources()
    ctx = f"# Context Index\n\n{load_text(CONTEXT)}\n\n---\n\n"
    for s in sources:
        ctx += f"# Source {s['id']}: {s['title']} (plane={s['plane']})\n\n{s['text']}\n\n---\n\n"
    graph = load_text(GRAPH)
    if graph:
        ctx += f"# Knowledge Graph\n\n```json\n{graph}\n```\n\n---\n\n"
    return ctx


def synthesize(model: str = "qwen2.5:1.5b") -> Path:
    """Generate a structured, source-grounded synthesis and save to synthesis.md."""
    out = BUNDLE / "synthesis.md"
    context = build_full_context()
    prompt = (
        "Bạn là NotebookLM — một mô hình đọc ngữ nghĩa (semantic read model). "
        "Tổng hợp toàn bộ tài liệu nguồn bên dưới thành một bản phân tích có cấu trúc, bao gồm:\n"
        "1. Tóm tắt tổng quan hệ thống Σ_APΩ (ngắn gọn, 4-6 bullet).\n"
        "2. Mind map phân cấp dạng markdown bullet (dùng #, ##, ###, -).\n"
        "3. Các mối quan hệ chủ đề chính và luồng nhân quả (2-3 bullet).\n"
        "4. Tối đa 5 câu hỏi khám phá tiếp theo, mỗi câu khác nhau, không lặp lại, kèm gợi ý trả lời từ nguồn.\n\n"
        "Quy tắc:\n"
        "- Chỉ sử dụng các tài liệu nguồn được cung cấp.\n"
        "- Không dùng kiến thức bên ngoài.\n"
        "- Trích dẫn nguồn bằng [NB-Sxx: tiêu đề tài liệu].\n"
        "- Không lặp lại câu hỏi hoặc ý.\n"
        "- Trả lời bằng tiếng Việt.\n\n"
        "--- TÀI LIỆU NGUỒN ---\n\n"
        f"{context}\n\n"
        "--- TỔNG HỢP ---\n"
    )
    answer = ollama_generate(prompt, model=model, timeout=600)
    header = f"> Synthesis generated by {model} from Σ_APΩ NotebookLM bundle.\n> Date: {_now()}\n\n"
    out.write_text(header + answer, encoding="utf-8")
    return out


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def brief_answer(question: str, top_k: int = 3, max_lines_per_source: int = 12) -> str:
    """Deterministic source-grounded brief. No LLM."""
    sources = load_sources()
    ranked = score_relevance(sources, question)
    selected = [s for _, s in ranked[:top_k]]

    lines = [
        f"# Source-grounded brief: {question}",
        "",
        "## Causal spine (from context_index.md)",
        "",
        "Observe → Diagnose → Plan → Approval Gate → Execute → Verify → Record",
        "",
        "## Relevant source documents",
        "",
    ]
    for s in selected:
        lines.append(f"- `{s['id']}` | plane={s['plane']} | {s['title']}")
    lines.append("")

    q = question.lower()
    for s in selected:
        lines.append(f"## Snippets from {s['id']} ({s['title']})")
        lines.append("")
        hits = 0
        for line in s["text"].splitlines():
            stripped = line.strip()
            if not stripped:
                continue
            score = sum(1 for word in re.findall(r"\w+", q) if word in stripped.lower())
            if score >= 1 and not stripped.startswith("-"):
                lines.append(f"> {stripped}")
                hits += 1
                if hits >= max_lines_per_source:
                    break
        if hits == 0:
            lines.append("_No direct keyword hit; source is topically related._")
        lines.append("")

    lines.extend([
        "## How to read this",
        "",
        "This brief is generated by matching the question against the six bounded source documents.",
        "It is not a second visual editor; the graph is data in `knowledge_graph.json`.",
        "For a generated narrative, use `--model <ollama-model>`.",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Query the Σ_APΩ NotebookLM bundle")
    parser.add_argument("--question", help="Question to answer from the corpus")
    parser.add_argument("--model", default="qwen2.5:1.5b", help="Ollama model to use")
    parser.add_argument("--top-k", type=int, default=4, help="Number of source documents to include")
    parser.add_argument("--raw-context", action="store_true", help="Print the retrieved context instead of generating")
    parser.add_argument("--brief", action="store_true", help="Generate deterministic source-grounded brief without LLM")
    parser.add_argument("--synth", action="store_true", help="Generate and save a structured synthesis of the whole bundle")
    args = parser.parse_args()

    if args.synth:
        out = synthesize(model=args.model)
        print(f"Synthesis written: {out}")
        return 0

    if not args.question:
        parser.error("--question is required (unless --synth)")

    if args.brief:
        print(brief_answer(args.question, top_k=args.top_k))
        return 0

    context = build_context(args.question, args.top_k)
    if args.raw_context:
        print(context)
        return 0

    prompt = build_prompt(context, args.question)
    answer = ollama_generate(prompt, model=args.model)
    print(answer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
