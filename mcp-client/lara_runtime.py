import json
import os
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
            model_override or os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash"),
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


async def run_query_once(
    user_query: str,
    provider_override: str | None = None,
    model_override: str | None = None,
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    temperature: float = 0.1,
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

            response = await llm_client.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=agent_tools,
                temperature=temperature,
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

                final_response = await llm_client.chat.completions.create(
                    model=model_name,
                    messages=messages,
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