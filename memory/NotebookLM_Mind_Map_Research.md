> Source: web research, 2026-07-28.
> Official docs: https://support.google.com/gemininotebook/answer/16212283
> Product home: https://notebooklm.google/
> Preserved as-is; do not normalize against external schemas.
> Author: Alpha_Prime_Omega

# NotebookLM / Gemini Notebook và Mind Map

## NotebookLM là gì

- AI-powered research assistant / "thinking partner" của Google.
- Grounded in sources: chỉ trả lời dựa trên tài liệu người dùng upload.
- Hỗ trợ PDF, website, YouTube, audio, Google Docs, Google Slides.
- Chức năng chính: summarize, Q&A with citations, Audio Overview, Mind Map.
- Không phải search engine, không dùng kiến thức bên ngoài sources trừ khi user bật "discover sources".

## Mind Map trong NotebookLM là gì

- **Visually summarize your uploaded sources**, hiển thị main topics và related ideas dưới dạng branching diagram.
- Mục đích:
  - Quick overview.
  - Explore and learn new topics easily.
  - Connect the dots (tìm liên kết không rõ ràng).
  - Organize your thoughts.
- Cách tạo:
  1. Mở notebook trong https://notebooklm.google.com/.
  2. Upload sources.
  3. Trong chat, chọn **Mind Map** chip.
  4. Mind Map xuất hiện trong Studio panel như một note.
- Tương tác:
  - Zoom, scroll.
  - Expand/collapse branches.
  - Double-click / select node để hỏi về chủ đề đó trong chat.
  - Download hoặc share notebook.
- Giới hạn:
  - Standard: 10 mind map/ngày.
  - Plus: 20.
  - Pro: 100.
  - Ultra: 500-1000.

## So sánh với Σ_APΩ integration

| Khía cạnh | NotebookLM gốc | Σ_APΩ integration |
|---|---|---|
| Sources | User upload thủ công | 6 bounded docs tự compile từ canon + evidence |
| Graph data | Không có sẵn API truy cập graph | `knowledge_graph.json` (knowledge/execution/connectors/evidence) |
| Mind map | Visual sinh bởi Gemini | Có thể upload bundle vào NotebookLM để nó sinh mind map; hoặc render Mermaid từ graph |
| Causal spine | Không | `context_index.md` Observe → Diagnose → Plan → Approval → Execute → Verify → Record |

## Mind map đã có chưa

- **Visual mind map** (hình ảnh/diagram) chưa có.
- **Dữ liệu mind map** đã có: `~/.axcanon/memory/notebooklm/knowledge_graph.json` + 6 source docs.
- Cần thì render từ `knowledge_graph.json` ra Mermaid mindmap, hoặc upload 6 sources vào NotebookLM và chọn Mind Map chip.
