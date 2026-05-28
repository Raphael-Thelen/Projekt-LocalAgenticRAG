import argparse
import asyncio
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CLIENT_DIR = ROOT / "mcp-client"
if str(CLIENT_DIR) not in sys.path:
    sys.path.insert(0, str(CLIENT_DIR))

from lara_runtime import run_query_with_forced_tool  # noqa: E402
from score_testbench import score_run  # noqa: E402

DEFAULT_SPEC = ROOT / "experiments" / "eval" / "testbench-v1.json"
RUNS_DIR = ROOT / "experiments" / "eval" / "runs"

TOOLS = [
    "search_exact_keyword",
    "search_fuzzy",
    "search_phrase_proximity",
]

MODES = ["user", "realistic_args", "diagnostic_args"]


def parse_tools(raw: str) -> list[str]:
    value = (raw or "all").strip().lower()
    if value == "all":
        return TOOLS[:]
    picked = [part.strip() for part in value.split(",") if part.strip()]
    invalid = [tool for tool in picked if tool not in TOOLS]
    if invalid:
        raise ValueError(f"Unsupported tool(s): {invalid}")
    return picked


def parse_mode(raw: str) -> str:
    mode = (raw or "realistic_args").strip().lower()
    if mode not in MODES:
        raise ValueError(f"Unsupported mode: {mode}. Allowed: {MODES}")
    return mode


def _trim_question(text: str) -> str:
    return " ".join(text.replace("?", " ").split()).strip()


def _build_user_args(question_text: str, tool: str) -> dict[str, Any]:
    q = question_text.strip()
    if tool in {"search_exact_keyword", "search_fuzzy"}:
        return {"query": q, "size": 5}
    return {"phrase": q, "slop": 8, "size": 5}


def _build_realistic_fallback_args(question_text: str, tool: str) -> dict[str, Any]:
    q = _trim_question(question_text)
    if tool == "search_exact_keyword":
        return {"query": q, "size": 5}
    if tool == "search_fuzzy":
        return {"query": q, "size": 5}
    short_phrase = " ".join(q.split()[:8]).strip()
    return {"phrase": short_phrase or q, "slop": 6, "size": 5}


def resolve_tool_args(question: dict[str, Any], tool: str, mode: str) -> dict[str, Any]:
    question_text = str(question.get("question", "")).strip()
    if mode == "user":
        return _build_user_args(question_text, tool)

    if mode == "realistic_args":
        realistic = question.get("realistic_tool_args", {})
        if isinstance(realistic, dict) and realistic.get(tool):
            return dict(realistic[tool])
        return _build_realistic_fallback_args(question_text, tool)

    diagnostic = question.get("diagnostic_tool_args", {})
    if isinstance(diagnostic, dict) and diagnostic.get(tool):
        return dict(diagnostic[tool])

    # Backward-compatible fallback for older specs.
    legacy = question.get("tool_args", {})
    if isinstance(legacy, dict) and legacy.get(tool):
        return dict(legacy[tool])
    return {}


def _first_line(text: str) -> str:
    line = (text or "").strip().splitlines()
    if not line:
        return ""
    return line[0].strip()


def resolve_expected_chunk_ids(question: dict[str, Any], tool: str) -> list[str]:
    chunk_goldtruth = question.get("chunk_goldtruth", {})

    if isinstance(chunk_goldtruth, dict):
        # Preferred compact format: one shared goldtruth per question.
        shared = chunk_goldtruth.get("shared")
        if isinstance(shared, dict):
            shared_ids = [str(cid) for cid in shared.get("expected_chunk_ids", [])]
            if shared_ids:
                return shared_ids

        # Backward-compatible aliases.
        for alias in ("all_tools", "global"):
            alias_row = chunk_goldtruth.get(alias)
            if isinstance(alias_row, dict):
                alias_ids = [str(cid) for cid in alias_row.get("expected_chunk_ids", [])]
                if alias_ids:
                    return alias_ids

        # Legacy per-tool format.
        tool_row = chunk_goldtruth.get(tool, {})
        if isinstance(tool_row, dict):
            return [str(cid) for cid in tool_row.get("expected_chunk_ids", [])]

    return []


def to_review_text(run_payload: dict[str, Any]) -> str:
    lines = [
        "MANUELLE BEWERTUNG (C/P/W)",
        "",
        "Regeln:",
        "- C = Correct (inhaltlich korrekt)",
        "- P = Partly correct (teilweise korrekt)",
        "- W = Wrong (falsch / nicht ausreichend)",
        "",
        "Wichtig:",
        "- Nur die RATING-Zeilen bearbeiten.",
        "- Format muss exakt bleiben: RATING|Qx|tool_name|C",
        "",
        f"Eval Mode: {run_payload.get('eval_mode', 'unknown')}",
        "",
    ]

    for question in run_payload.get("questions", []):
        lines.extend(
            [
                f"========{question['id']}=======",
                question.get("question", ""),
                "",
                f"Expected: {question.get('expected_answer', '')}",
            ]
        )

        answer_rule = question.get("answer_rule", "")
        if answer_rule:
            lines.extend(["", f"Answer Rule: {answer_rule}"])

        lines.append("")

        tool_results = question.get("tool_results", {})
        for tool in TOOLS:
            if tool not in tool_results:
                continue
            row = tool_results[tool]
            lines.extend(
                [
                    f"--------{tool}--------",
                    f"AI-Answer: {row.get('answer', '')}",
                    "",
                    f"RATING|{question['id']}|{tool}|?",
                    "",
                ]
            )

        lines.append("")

    return "\n".join(lines)


async def run_testbench(
    spec_path: Path,
    provider: str,
    model: str | None,
    tools: list[str],
    mode: str,
    max_retries: int,
    retry_base_seconds: float,
    retry_max_seconds: float,
    retry_jitter_seconds: float,
    skip_llm_on_zero_hits: bool,
    top_k_context: int,
) -> dict[str, Any]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id_with_mode = f"{run_id}-{mode}"
    run_dir = RUNS_DIR / run_id_with_mode
    run_dir.mkdir(parents=True, exist_ok=False)

    run_payload: dict[str, Any] = {
        "run_id": run_id_with_mode,
        "run_id_base": run_id,
        "created_at": datetime.now().isoformat(),
        "spec_path": str(spec_path),
        "eval_mode": mode,
        "provider": provider,
        "provider_label": "pending",
        "model": model or "default",
        "selected_tools": tools,
        "retry_policy": {
            "max_retries": max_retries,
            "retry_base_seconds": retry_base_seconds,
            "retry_max_seconds": retry_max_seconds,
            "retry_jitter_seconds": retry_jitter_seconds,
        },
        "skip_llm_on_zero_hits": skip_llm_on_zero_hits,
        "questions": [],
    }

    print("=" * 80)
    print("Testbench gestartet")
    print(f"Mode: {mode}")
    print(f"Provider/Model: {provider}/{model or 'default'}")
    print(f"Tools: {', '.join(tools)}")
    print(f"Fragen gesamt: {len(spec.get('questions', []))}")
    print(f"Skip LLM on 0 hits: {skip_llm_on_zero_hits}")
    print(f"Run-Ordner: {run_dir}")
    print("=" * 80)

    for q_index, question in enumerate(spec.get("questions", [])):
        qid = str(question.get("id", f"Q{q_index + 1}"))
        q_text = str(question.get("question", "")).strip()
        q_expected = str(question.get("expected_answer", "")).strip()
        q_out: dict[str, Any] = {
            "id": qid,
            "category": question.get("category", ""),
            "difficulty": question.get("difficulty", ""),
            "question": q_text,
            "expected_answer": q_expected,
            "answer_rule": question.get("answer_rule", ""),
            "tool_results": {},
        }

        print("")
        print(f"[{q_index + 1}/{len(spec.get('questions', []))}] {qid}")
        print(f"Frage: {q_text}")

        for tool in tools:
            args = resolve_tool_args(question, tool, mode)
            if not args:
                print(f"  - {tool}: uebersprungen (keine Args im Modus {mode})")
                continue

            print(f"  - {tool}: starte Retrieval mit Args {json.dumps(args, ensure_ascii=True)}")

            result = await run_query_with_forced_tool(
                user_query=q_text,
                tool_name=tool,
                tool_args=args,
                provider_override=provider,
                model_override=model,
                temperature=0.1,
                top_k_context=top_k_context,
                skip_llm_on_zero_hits=skip_llm_on_zero_hits,
                max_retries=max_retries,
                retry_base_seconds=retry_base_seconds,
                retry_max_seconds=retry_max_seconds,
                retry_jitter_seconds=retry_jitter_seconds,
                verbose_retry=True,
            )

            if run_payload["provider_label"] == "pending":
                run_payload["provider"] = result.get("provider", provider)
                run_payload["provider_label"] = result.get("provider_label", provider)
                run_payload["model"] = result.get("model", model or "default")

            retrieved_count = int(result.get("retrieved_count", 0))
            print(f"    Retrieval fertig: {retrieved_count} Treffer")
            if result.get("llm_skipped", False):
                print("    LLM uebersprungen: 0 Retrieval-Treffer")
            else:
                print(f"    Antwort erste Zeile: {_first_line(str(result.get('answer', '')))}")

            expected_chunk_ids = resolve_expected_chunk_ids(question, tool)

            q_out["tool_results"][tool] = {
                "tool_args": args,
                "retrieved_count": retrieved_count,
                "retrieved_chunk_ids": [
                    str(cid) for cid in result.get("retrieved_chunk_ids", [])
                ],
                "expected_chunk_ids": expected_chunk_ids,
                "retrieval_payload": result.get("retrieval_payload", {"count": 0, "results": []}),
                "answer": str(result.get("answer", "")).strip(),
                "llm_skipped": bool(result.get("llm_skipped", False)),
            }

        print(f"[{qid}] abgeschlossen")

        run_payload["questions"].append(q_out)

    run_json = run_dir / f"run-{mode}.json"
    review_txt = run_dir / f"manual-review-{mode}.txt"
    run_json.write_text(json.dumps(run_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    review_txt.write_text(to_review_text(run_payload), encoding="utf-8")

    return {
        "run_id": run_id_with_mode,
        "eval_mode": mode,
        "run_dir": str(run_dir),
        "run_json": str(run_json),
        "review_txt": str(review_txt),
    }


def open_editor_wait(path: Path) -> None:
    code_cmd = shutil.which("code")
    if code_cmd:
        subprocess.run([code_cmd, "--wait", str(path)], check=True)
        return

    print(f"Bitte die Datei manuell oeffnen und speichern: {path}")
    input("Wenn die Bewertung fertig ist, Enter druecken ... ")


async def main_async(args: argparse.Namespace) -> None:
    tools = parse_tools(args.tools)
    mode = parse_mode(args.mode)
    result = await run_testbench(
        spec_path=args.spec,
        provider=args.provider,
        model=args.model,
        tools=tools,
        mode=mode,
        max_retries=args.max_retries,
        retry_base_seconds=args.retry_base_seconds,
        retry_max_seconds=args.retry_max_seconds,
        retry_jitter_seconds=args.retry_jitter_seconds,
        skip_llm_on_zero_hits=args.skip_llm_on_zero_hits,
        top_k_context=args.top_k_context,
    )

    print(f"Wrote {result['run_json']}")
    print(f"Wrote {result['review_txt']}")

    if args.score_after_review:
        review_path = Path(result["review_txt"])
        run_json_path = Path(result["run_json"])
        open_editor_wait(review_path)
        score = score_run(run_json_path, review_path)
        print(f"Wrote {score['score_json']}")
        print(f"Wrote {score['score_txt']}")
        review_path.unlink(missing_ok=True)
        print(f"Deleted {review_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run testbench and generate manual review file.")
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--provider", choices=["gemini", "ollama"], default="gemini")
    parser.add_argument("--model", type=str)
    parser.add_argument(
        "--tools",
        type=str,
        default="all",
        help="all or comma separated: search_exact_keyword,search_fuzzy,search_phrase_proximity",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="realistic_args",
        help="Evaluation mode: user, realistic_args, diagnostic_args",
    )
    parser.add_argument("--max-retries", type=int, default=12)
    parser.add_argument("--retry-base-seconds", type=float, default=20.0)
    parser.add_argument("--retry-max-seconds", type=float, default=300.0)
    parser.add_argument("--retry-jitter-seconds", type=float, default=3.0)
    parser.add_argument(
        "--skip-llm-on-zero-hits",
        dest="skip_llm_on_zero_hits",
        action="store_true",
        help="Skip LLM calls when retrieval has zero hits (default).",
    )
    parser.add_argument(
        "--no-skip-llm-on-zero-hits",
        dest="skip_llm_on_zero_hits",
        action="store_false",
        help="Still call LLM even when retrieval has zero hits.",
    )
    parser.set_defaults(skip_llm_on_zero_hits=True)
    parser.add_argument("--top-k-context", type=int, default=5)
    parser.add_argument("--score-after-review", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main_async(args))
