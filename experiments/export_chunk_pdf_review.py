import argparse
import json
from pathlib import Path
from typing import Any


def shorten(text: str, max_len: int = 260) -> str:
    clean = " ".join(text.split())
    if len(clean) <= max_len:
        return clean
    return clean[: max_len - 3] + "..."


def unique_by_chunk(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in results:
        cid = str(row.get("chunk_id", ""))
        if not cid:
            continue
        if cid in seen:
            continue
        seen.add(cid)
        out.append(row)
    return out


def build_review_md(run_payload: dict[str, Any], pdf_path: str | None) -> str:
    lines: list[str] = []
    lines.append("# Chunk-to-PDF Review")
    lines.append("")
    lines.append(f"Run ID: {run_payload.get('run_id', 'unknown')}")
    lines.append(f"Eval Mode: {run_payload.get('eval_mode', 'unknown')}")
    if pdf_path:
        lines.append(f"PDF: {pdf_path}")
    lines.append("")
    lines.append("Hinweis: Seite stammt aus dem Index-Feld 'page'. Chunk-ID enthält ebenfalls die Seite als Muster _p<seite>_.")
    lines.append("")

    for q in run_payload.get("questions", []):
        qid = str(q.get("id", ""))
        question = str(q.get("question", ""))
        lines.append(f"## {qid}: {question}")
        lines.append("")

        tool_results = q.get("tool_results", {})
        for tool_name, tool_row in tool_results.items():
            lines.append(f"### Tool: {tool_name}")
            lines.append("")

            retrieval_payload = tool_row.get("retrieval_payload", {})
            results = retrieval_payload.get("results", [])
            unique_results = unique_by_chunk(results)

            if not unique_results:
                lines.append("Keine Treffer.")
                lines.append("")
                continue

            lines.append("| Rank | Chunk ID | Seite | Score | Quelle | Excerpt |")
            lines.append("|---:|---|---:|---:|---|---|")
            for idx, hit in enumerate(unique_results, start=1):
                chunk_id = str(hit.get("chunk_id", ""))
                page = hit.get("page", "")
                score = hit.get("score", "")
                source = str(hit.get("source", ""))
                excerpt = shorten(str(hit.get("excerpt", ""))).replace("|", "\\|")
                lines.append(f"| {idx} | {chunk_id} | {page} | {score} | {source} | {excerpt} |")

            lines.append("")
            lines.append("Markiere die relevanten Chunk-IDs als Gold und übertrage sie in testbench-v1.json -> chunk_goldtruth -> expected_chunk_ids.")
            lines.append("")

        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Exportiert eine Chunk-PDF-Review-Datei aus einem Testbench-Run.")
    parser.add_argument("--run-json", type=Path, required=True, help="Pfad zu run-<mode>.json")
    parser.add_argument("--output", type=Path, default=None, help="Zielpfad fuer die Review-Datei (.md)")
    parser.add_argument("--pdf-path", type=str, default=None, help="Optional: Referenz auf das Original-PDF")
    args = parser.parse_args()

    run_payload = json.loads(args.run_json.read_text(encoding="utf-8"))

    if args.output is None:
        mode = str(run_payload.get("eval_mode", "unknown"))
        out_path = args.run_json.parent / f"chunk-pdf-review-{mode}.md"
    else:
        out_path = args.output

    review_md = build_review_md(run_payload, args.pdf_path)
    out_path.write_text(review_md + "\n", encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
