import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RATING_RE = re.compile(r"^RATING\|(?P<qid>[^|]+)\|(?P<tool>[^|]+)\|(?P<rating>[CPW\?])$")


@dataclass
class FlatRow:
    question_id: str
    tool: str
    retrieved_chunk_ids: list[str]
    expected_chunk_ids: list[str]
    rating: str


def parse_review_ratings(review_txt: Path) -> dict[tuple[str, str], str]:
    ratings: dict[tuple[str, str], str] = {}
    for raw_line in review_txt.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        match = RATING_RE.match(line)
        if not match:
            continue
        qid = match.group("qid").strip()
        tool = match.group("tool").strip()
        rating = match.group("rating").strip()
        ratings[(qid, tool)] = rating
    return ratings


def flatten_run(run_payload: dict[str, Any], ratings: dict[tuple[str, str], str]) -> list[FlatRow]:
    rows: list[FlatRow] = []

    for qrow in run_payload.get("questions", []):
        qid = str(qrow.get("id", ""))
        tool_results = qrow.get("tool_results", {})

        for tool, trow in tool_results.items():
            retrieved = [str(x) for x in trow.get("retrieved_chunk_ids", [])]
            expected = [str(x) for x in trow.get("expected_chunk_ids", [])]
            rating = ratings.get((qid, tool), "?")
            rows.append(
                FlatRow(
                    question_id=qid,
                    tool=tool,
                    retrieved_chunk_ids=retrieved,
                    expected_chunk_ids=expected,
                    rating=rating,
                )
            )

    return rows


def apply_ratings_to_run_payload(
    run_payload: dict[str, Any],
    ratings: dict[tuple[str, str], str],
) -> dict[str, Any]:
    for qrow in run_payload.get("questions", []):
        qid = str(qrow.get("id", ""))
        tool_results = qrow.get("tool_results", {})
        for tool, trow in tool_results.items():
            rating = ratings.get((qid, tool), "?")
            trow["manual_rating"] = rating
    return run_payload


def retrieval_metrics(rows: list[FlatRow]) -> dict[str, Any]:
    eval_rows = [row for row in rows if row.expected_chunk_ids]

    if not eval_rows:
        return {
            "evaluated_rows": 0,
            "macro_precision": None,
            "macro_recall": None,
            "hit_rate": None,
        }

    p_vals: list[float] = []
    r_vals: list[float] = []
    h_vals: list[float] = []

    for row in eval_rows:
        expected = set(row.expected_chunk_ids)
        retrieved = row.retrieved_chunk_ids
        rel_count = sum(1 for cid in retrieved if cid in expected)

        precision = rel_count / len(retrieved) if retrieved else 0.0
        recall = rel_count / len(expected) if expected else 0.0
        hit = 1.0 if rel_count > 0 else 0.0

        p_vals.append(precision)
        r_vals.append(recall)
        h_vals.append(hit)

    return {
        "evaluated_rows": len(eval_rows),
        "macro_precision": sum(p_vals) / len(p_vals),
        "macro_recall": sum(r_vals) / len(r_vals),
        "hit_rate": sum(h_vals) / len(h_vals),
    }


def answer_metrics(rows: list[FlatRow]) -> dict[str, Any]:
    rated = [row for row in rows if row.rating in {"C", "P", "W"}]

    if not rated:
        return {
            "rated_rows": 0,
            "count_C": 0,
            "count_P": 0,
            "count_W": 0,
            "strict_precision": None,
            "lenient_recall": None,
            "weighted_score": None,
        }

    c = sum(1 for row in rated if row.rating == "C")
    p = sum(1 for row in rated if row.rating == "P")
    w = sum(1 for row in rated if row.rating == "W")
    total = len(rated)

    strict_precision = c / total
    lenient_recall = (c + p) / total
    weighted_score = (1.0 * c + 0.5 * p + 0.0 * w) / total

    return {
        "rated_rows": total,
        "count_C": c,
        "count_P": p,
        "count_W": w,
        "strict_precision": strict_precision,
        "lenient_recall": lenient_recall,
        "weighted_score": weighted_score,
    }


def by_tool(rows: list[FlatRow]) -> dict[str, Any]:
    tools = sorted({row.tool for row in rows})
    out: dict[str, Any] = {}
    for tool in tools:
        subset = [row for row in rows if row.tool == tool]
        out[tool] = {
            "retrieval": retrieval_metrics(subset),
            "answer": answer_metrics(subset),
        }
    return out


def to_summary_text(score_payload: dict[str, Any]) -> str:
    def fmt(value: Any) -> str:
        if value is None:
            return "n/a"
        if isinstance(value, float):
            return f"{value:.3f}"
        return str(value)

    lines = [
        "Testbench Score Summary",
        "",
        f"Run ID: {score_payload['run_id']}",
        f"Eval Mode: {score_payload.get('eval_mode', 'unknown')}",
        f"Spec: {score_payload['spec_path']}",
        f"Run File: {score_payload['run_json_path']}",
        f"Review File: {score_payload['review_txt_path']}",
        "",
        "Overall Retrieval",
        f"- Evaluated Rows: {fmt(score_payload['overall']['retrieval']['evaluated_rows'])}",
        f"- Macro Precision: {fmt(score_payload['overall']['retrieval']['macro_precision'])}",
        f"- Macro Recall: {fmt(score_payload['overall']['retrieval']['macro_recall'])}",
        f"- Hit Rate: {fmt(score_payload['overall']['retrieval']['hit_rate'])}",
        "",
        "Overall Answer",
        f"- Rated Rows: {fmt(score_payload['overall']['answer']['rated_rows'])}",
        f"- C/P/W: {fmt(score_payload['overall']['answer']['count_C'])}/{fmt(score_payload['overall']['answer']['count_P'])}/{fmt(score_payload['overall']['answer']['count_W'])}",
        f"- Strict Precision (C only): {fmt(score_payload['overall']['answer']['strict_precision'])}",
        f"- Lenient Recall (C+P): {fmt(score_payload['overall']['answer']['lenient_recall'])}",
        f"- Weighted Score (C=1,P=0.5,W=0): {fmt(score_payload['overall']['answer']['weighted_score'])}",
        "",
        "By Tool",
    ]

    for tool, metrics in score_payload["by_tool"].items():
        lines.extend(
            [
                "",
                f"[{tool}]",
                f"- Retrieval Macro Precision: {fmt(metrics['retrieval']['macro_precision'])}",
                f"- Retrieval Macro Recall: {fmt(metrics['retrieval']['macro_recall'])}",
                f"- Retrieval Hit Rate: {fmt(metrics['retrieval']['hit_rate'])}",
                f"- Answer C/P/W: {fmt(metrics['answer']['count_C'])}/{fmt(metrics['answer']['count_P'])}/{fmt(metrics['answer']['count_W'])}",
                f"- Answer Strict Precision: {fmt(metrics['answer']['strict_precision'])}",
                f"- Answer Lenient Recall: {fmt(metrics['answer']['lenient_recall'])}",
                f"- Answer Weighted Score: {fmt(metrics['answer']['weighted_score'])}",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def score_run(run_json: Path, review_txt: Path) -> dict[str, Any]:
    run_payload = json.loads(run_json.read_text(encoding="utf-8"))
    ratings = parse_review_ratings(review_txt)
    run_payload = apply_ratings_to_run_payload(run_payload, ratings)
    run_json.write_text(json.dumps(run_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    rows = flatten_run(run_payload, ratings)
    eval_mode = str(run_payload.get("eval_mode", "unknown"))

    score_payload = {
        "run_id": run_payload.get("run_id", "unknown"),
        "eval_mode": eval_mode,
        "spec_path": run_payload.get("spec_path", "unknown"),
        "run_json_path": str(run_json),
        "review_txt_path": str(review_txt),
        "overall": {
            "retrieval": retrieval_metrics(rows),
            "answer": answer_metrics(rows),
        },
        "by_tool": by_tool(rows),
    }

    score_json = run_json.parent / f"score-{eval_mode}.json"
    score_txt = run_json.parent / f"score-summary-{eval_mode}.txt"

    score_json.write_text(json.dumps(score_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    score_txt.write_text(to_summary_text(score_payload), encoding="utf-8")

    return {
        "score_json": str(score_json),
        "score_txt": str(score_txt),
        "score": score_payload,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Score one testbench run after manual C/P/W review.")
    parser.add_argument("--run-json", type=Path, required=True)
    parser.add_argument("--review-txt", type=Path, required=True)
    args = parser.parse_args()

    result = score_run(args.run_json, args.review_txt)
    print(f"Wrote {result['score_json']}")
    print(f"Wrote {result['score_txt']}")
