import asyncio
import json
import os
import random
import re
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


ROOT = Path(__file__).resolve().parents[1]
MCP_SERVER_SCRIPT = ROOT / "mcp-server" / "index.ts"
DEFAULT_SYSTEM_PROMPT = (
    "Du bist L.A.R.A., ein praeziser, lokaler Forschungs-Assistent. "
    "Antworte immer auf Deutsch. Nutze dein Such-Tool, um in den "
    "lokalen Dokumenten nach Fakten zu suchen, bevor du antwortest. "
    "Vermeide es zu halluzinieren."
)


def load_env_file() -> None:
    """Laedt optionale .env aus dem Projekt-Root ohne Zusatzabhaengigkeiten."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        return

    with env_path.open("r", encoding="utf-8") as env_file:
        for raw_line in env_file:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()


def _is_retryable_quota_error(exc: Exception) -> bool:
    text = str(exc).lower()
    markers = [
        "quota",
        "rate limit",
        "rate_limit",
        "too many requests",
        "resource has been exhausted",
        "429",
    ]
    return any(marker in text for marker in markers)


def _parse_retry_after_from_error(exc: Exception) -> float | None:
    response = getattr(exc, "response", None)
    if response is not None:
        headers = getattr(response, "headers", None)
        if headers:
            retry_after = headers.get("retry-after") or headers.get("Retry-After")
            if retry_after:
                try:
                    return max(0.0, float(retry_after))
                except ValueError:
                    pass

    text = str(exc)
    patterns = [
        r"retry\s+(?:in|after)\s+(\d+(?:\.\d+)?)\s*s",
        r"retry_delay.*?seconds\D+(\d+)",
        r'"seconds"\s*:\s*(\d+)',
    ]
    lowered = text.lower()
    for pattern in patterns:
        match = re.search(pattern, lowered)
        if match:
            try:
                return max(0.0, float(match.group(1)))
            except ValueError:
                continue
    return None


async def _chat_with_retry(
    llm_client: AsyncOpenAI,
    *,
    model: str,
    messages: list[Any],
    tools: list[dict[str, Any]] | None = None,
    temperature: float | None = None,
    max_retries: int = 12,
    retry_base_seconds: float = 20.0,
    retry_max_seconds: float = 300.0,
    retry_jitter_seconds: float = 3.0,
    verbose: bool = False,
    operation_label: str = "llm_chat",
) -> Any:
    attempt = 0
    while True:
        try:
            kwargs: dict[str, Any] = {
                "model": model,
                "messages": messages,
            }
            if tools is not None:
                kwargs["tools"] = tools
            if temperature is not None:
                kwargs["temperature"] = temperature
            if verbose and attempt == 0:
                print(
                    f"[LARA][{operation_label}] Sende Anfrage an Modell {model}..."
                )
            return await llm_client.chat.completions.create(**kwargs)
        except Exception as exc:
            retryable = _is_retryable_quota_error(exc)
            err_class = type(exc).__name__
            err_text = " ".join(str(exc).split())
            err_preview = err_text[:500] + ("..." if len(err_text) > 500 else "")

            if verbose:
                print(
                    f"[LARA][{operation_label}] Fehler: {err_class}: {err_preview}"
                )

            if not retryable or attempt >= max_retries:
                if verbose:
                    if not retryable:
                        print(
                            f"[LARA][{operation_label}] Fehler ist nicht retry-faehig. Breche ab."
                        )
                    else:
                        print(
                            f"[LARA][{operation_label}] Max Retries erreicht "
                            f"({max_retries}). Breche ab."
                        )
                raise

            server_wait = _parse_retry_after_from_error(exc)
            exp_wait = min(retry_max_seconds, retry_base_seconds * (2**attempt))
            jitter = random.uniform(0.0, max(0.0, retry_jitter_seconds))
            wait_seconds = max(server_wait or 0.0, exp_wait) + jitter

            if verbose:
                print(
                    f"[LARA][{operation_label}] Quota/Rate-Limit erkannt. "
                    f"Retry {attempt + 1}/{max_retries} in {wait_seconds:.1f}s "
                    f"(retry_after={server_wait}, exp_backoff={exp_wait:.1f}, jitter={jitter:.1f})"
                )

            await asyncio.sleep(wait_seconds)
            attempt += 1


def _build_context_from_results(results: list[dict], limit: int = 5) -> str:
    lines = [
        "Kontext aus lokalen Dokumenten (MCP Retrieval):",
        "",
    ]

    for idx, row in enumerate(results[:limit], start=1):
        title = str(row.get("title", "unknown"))
        page = row.get("page", None)
        chunk_id = str(row.get("chunk_id", "unknown"))
        excerpt = " ".join(str(row.get("excerpt", "")).split())
        lines.append(f"[{idx}] title={title} | page={page} | chunk_id={chunk_id}")
        lines.append(f"excerpt: {excerpt}")
        lines.append("")

    return "\n".join(lines).strip()


def resolve_provider(provider_override: str | None = None) -> str:
    provider = provider_override or os.getenv("LARA_LLM_PROVIDER", "gemini")
    return provider.strip().lower()


def build_llm_client(
    provider_override: str | None = None,
    model_override: str | None = None,
) -> tuple[AsyncOpenAI, str, str, str]:
    """Erstellt LLM-Client + Modellname je nach gewaehltem Provider."""
    provider = resolve_provider(provider_override)

    if provider == "gemini":
        gemini_api_key = os.getenv("GEMINI_API_KEY", "")
        if not gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY fehlt. Bitte in der Shell oder .env setzen."
            )

        return (
            AsyncOpenAI(
                base_url=os.getenv(
                    "GEMINI_BASE_URL",
                    "https://generativelanguage.googleapis.com/v1beta/openai/",
                ),
                api_key=gemini_api_key,
            ),
            model_override or os.getenv("GEMINI_MODEL_NAME", "gemini-3.1-flash-lite"),
            "Gemini API",
            provider,
        )

    if provider == "ollama":
        return (
            AsyncOpenAI(
                base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
                api_key="LokalBrauchenWirKeinenKey",
            ),
            model_override or os.getenv("OLLAMA_MODEL_NAME", "llama3.1"),
            "Ollama lokal",
            provider,
        )

    raise RuntimeError(
        "Unbekannter LARA_LLM_PROVIDER. Erlaubt sind: gemini, ollama"
    )


async def _plan_smart_query_with_same_llm(
    llm_client: AsyncOpenAI,
    *,
    model: str,
    user_query: str,
    requested_top_k: int,
    max_retries: int,
    retry_base_seconds: float,
    retry_max_seconds: float,
    retry_jitter_seconds: float,
    verbose: bool,
) -> dict[str, Any] | None:
    planner_prompt = (
        "Du bist Query-Planer fuer Elasticsearch in der DSA/Aventurien-Domaene. "
        "Gib ausschliesslich JSON mit exakt diesen Feldern zurueck: "
        "normalized_query, keyword_terms, expanded_terms, retrieval_mode, top_k, confidence, rationale. "
        "retrieval_mode muss einer von fuzzy_only|fuzzy_plus_exact|balanced sein. "
        "Lege retrieval_mode eigenstaendig fest nach der Nutzerfrage: "
        "fuzzy_only fuer unscharfe/allgemeine Fragen, "
        "fuzzy_plus_exact fuer konkrete Regel-/Zahlen-/Begriffsfragen, "
        "balanced fuer Mischfaelle aus Begriff + Kontext. "
        "Beruecksichtige Schreibvarianten wie fuer/f\u00fcr und zwoelfgoetter/zw\u00f6lfgoetter. "
        "keyword_terms sollen praezise Suchanker sein (2-6), expanded_terms sinnvolle Varianten/Synonyme (3-10)."
    )

    messages: list[dict[str, str]] = [
        {"role": "system", "content": planner_prompt},
        {
            "role": "user",
            "content": (
                f"Frage: {user_query}\n"
                f"TopK: {requested_top_k}\n"
                "JSON only."
            ),
        },
    ]

    try:
        response = await _chat_with_retry(
            llm_client,
            model=model,
            messages=messages,
            temperature=0.2,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
            retry_max_seconds=retry_max_seconds,
            retry_jitter_seconds=retry_jitter_seconds,
            verbose=verbose,
            operation_label="smart_query_planner",
        )
    except Exception:
        return None

    raw = (response.choices[0].message.content or "").strip()
    if not raw:
        return None

    parsed: dict[str, Any] | None = None
    try:
        loaded = json.loads(raw)
        if isinstance(loaded, dict):
            parsed = loaded
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            try:
                loaded = json.loads(raw[start : end + 1])
                if isinstance(loaded, dict):
                    parsed = loaded
            except json.JSONDecodeError:
                parsed = None

    if not parsed:
        return None

    normalized_query = str(parsed.get("normalized_query", "")).strip()
    if not normalized_query:
        return None

    mode = str(parsed.get("retrieval_mode", "")).strip().lower()
    if mode not in {"fuzzy_only", "fuzzy_plus_exact", "balanced"}:
        return None

    keyword_terms_raw = parsed.get("keyword_terms", [])
    expanded_terms_raw = parsed.get("expanded_terms", [])
    keyword_terms = [str(x).strip().lower() for x in keyword_terms_raw if str(x).strip()][:12]
    expanded_terms = [str(x).strip().lower() for x in expanded_terms_raw if str(x).strip()][:12]

    top_k_raw = parsed.get("top_k", requested_top_k)
    try:
        top_k = max(1, min(20, int(top_k_raw)))
    except (TypeError, ValueError):
        top_k = max(1, min(20, int(requested_top_k)))

    confidence_raw = parsed.get("confidence", 0.5)
    try:
        confidence = float(confidence_raw)
    except (TypeError, ValueError):
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    rationale = str(parsed.get("rationale", "client_planned")).strip()[:300] or "client_planned"

    return {
        "normalized_query": normalized_query,
        "keyword_terms": keyword_terms,
        "expanded_terms": expanded_terms,
        "retrieval_mode": mode,
        "top_k": top_k,
        "confidence": confidence,
        "rationale": rationale,
    }


async def run_query_once(
    user_query: str,
    provider_override: str | None = None,
    model_override: str | None = None,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    temperature: float = 0.1,
    max_retries: int = 12,
    retry_base_seconds: float = 20.0,
    retry_max_seconds: float = 300.0,
    retry_jitter_seconds: float = 3.0,
    verbose_retry: bool = False,
) -> dict[str, Any]:
    llm_client, model_name, provider_label, provider_key = build_llm_client(
        provider_override=provider_override,
        model_override=model_override,
    )

    server_params = StdioServerParameters(
        command="npx",
        args=["tsx", str(MCP_SERVER_SCRIPT)],
        cwd=str(ROOT / "mcp-server"),
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools_response = await session.list_tools()
            agent_tools = []
            tool_names = []
            for tool in tools_response.tools:
                tool_names.append(tool.name)
                agent_tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": tool.inputSchema,
                        },
                    }
                )

            messages: list[Any] = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ]

            response = await _chat_with_retry(
                llm_client,
                model=model_name,
                messages=messages,
                tools=agent_tools,
                temperature=temperature,
                max_retries=max_retries,
                retry_base_seconds=retry_base_seconds,
                retry_max_seconds=retry_max_seconds,
                retry_jitter_seconds=retry_jitter_seconds,
                verbose=verbose_retry,
                operation_label="agent_first_call",
            )

            response_message = response.choices[0].message
            messages.append(response_message)

            tool_calls_trace: list[dict[str, Any]] = []
            final_answer = response_message.content or ""

            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    tool_result = await session.call_tool(tool_name, tool_args)
                    result_text = "\n".join(
                        [
                            content.text
                            for content in tool_result.content
                            if content.type == "text"
                        ]
                    )

                    tool_calls_trace.append(
                        {
                            "name": tool_name,
                            "args": tool_args,
                            "result_chars": len(result_text),
                            "result_preview": result_text[:500],
                        }
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result_text,
                        }
                    )

                final_response = await _chat_with_retry(
                    llm_client,
                    model=model_name,
                    messages=messages,
                    max_retries=max_retries,
                    retry_base_seconds=retry_base_seconds,
                    retry_max_seconds=retry_max_seconds,
                    retry_jitter_seconds=retry_jitter_seconds,
                    verbose=verbose_retry,
                    operation_label="agent_final_call",
                )
                final_answer = final_response.choices[0].message.content or ""

            return {
                "provider": provider_key,
                "provider_label": provider_label,
                "model": model_name,
                "available_tools": tool_names,
                "tool_calls": tool_calls_trace,
                "final_answer": final_answer,
            }


async def run_query_with_forced_tool(
    user_query: str,
    tool_name: str,
    tool_args: dict[str, Any],
    provider_override: str | None = None,
    model_override: str | None = None,
    temperature: float = 0.1,
    top_k_context: int = 5,
    skip_llm_on_zero_hits: bool = True,
    max_retries: int = 12,
    retry_base_seconds: float = 20.0,
    retry_max_seconds: float = 300.0,
    retry_jitter_seconds: float = 3.0,
    verbose_retry: bool = False,
) -> dict[str, Any]:
    llm_client, model_name, provider_label, provider_key = build_llm_client(
        provider_override=provider_override,
        model_override=model_override,
    )

    server_params = StdioServerParameters(
        command="npx",
        args=["tsx", str(MCP_SERVER_SCRIPT)],
        cwd=str(ROOT / "mcp-server"),
    )

    call_args = dict(tool_args)
    if tool_name == "search_smart":
        requested_top_k = call_args.get("size", 5)
        try:
            requested_top_k_int = int(requested_top_k)
        except (TypeError, ValueError):
            requested_top_k_int = 5

        smart_plan = await _plan_smart_query_with_same_llm(
            llm_client,
            model=model_name,
            user_query=user_query,
            requested_top_k=requested_top_k_int,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
            retry_max_seconds=retry_max_seconds,
            retry_jitter_seconds=retry_jitter_seconds,
            verbose=verbose_retry,
        )
        if smart_plan:
            call_args["plan"] = smart_plan
            call_args["planner_source"] = f"client_{provider_key}"

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tool_result = await session.call_tool(tool_name, call_args)
            text_blocks = [item.text for item in tool_result.content if item.type == "text"]
            payload: dict[str, Any] = {"count": 0, "results": []}
            if text_blocks:
                first_block = text_blocks[0].strip()
                try:
                    payload = json.loads(first_block)
                except json.JSONDecodeError:
                    payload = {
                        "count": 0,
                        "results": [],
                        "error": first_block,
                    }

            if not isinstance(payload, dict):
                payload = {
                    "count": 0,
                    "results": [],
                    "error": "Tool payload was not a JSON object.",
                }

            results_raw = payload.get("results", [])
            results = results_raw if isinstance(results_raw, list) else []
            count_raw = payload.get("count", len(results))
            try:
                retrieved_count = int(count_raw)
            except (TypeError, ValueError):
                retrieved_count = len(results)
            context_text = _build_context_from_results(results, limit=top_k_context)

            if skip_llm_on_zero_hits and retrieved_count == 0:
                answer = (
                    "Keine Treffer im Retrieval. Es wurde kein LLM-Aufruf gemacht, "
                    "um Quota zu schonen."
                )
                llm_skipped = True
            else:
                llm_messages: list[dict[str, str]] = [
                    {
                        "role": "system",
                        "content": (
                            "Du bist ein praeziser Assistent fuer DSA-Regelfragen. "
                            "Antworte kurz, faktisch und auf Deutsch. "
                            "Nutze nur den bereitgestellten Kontext. "
                            "Wenn der Kontext nicht ausreicht, sage das klar."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Frage: {user_query}\n\n"
                            f"{context_text}\n\n"
                            "Bitte beantworte die Frage praezise."
                        ),
                    },
                ]

                llm_response = await _chat_with_retry(
                    llm_client,
                    model=model_name,
                    messages=llm_messages,
                    temperature=temperature,
                    max_retries=max_retries,
                    retry_base_seconds=retry_base_seconds,
                    retry_max_seconds=retry_max_seconds,
                    retry_jitter_seconds=retry_jitter_seconds,
                    verbose=verbose_retry,
                    operation_label=f"forced_tool:{tool_name}",
                )
                answer = llm_response.choices[0].message.content or ""
                llm_skipped = False

            return {
                "provider": provider_key,
                "provider_label": provider_label,
                "model": model_name,
                "tool": tool_name,
                "tool_args": call_args,
                "retrieval_payload": payload,
                "retrieved_count": retrieved_count,
                "retrieved_chunk_ids": [
                    str(row.get("chunk_id", "")) for row in results if row.get("chunk_id")
                ],
                "answer": (answer or "").strip(),
                "llm_skipped": llm_skipped,
            }