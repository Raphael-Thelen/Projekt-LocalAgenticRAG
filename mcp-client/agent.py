import argparse
import asyncio

from lara_runtime import resolve_provider, run_query_once


async def run_agentic_loop(
    user_query: str,
    provider_override: str | None = None,
    model_override: str | None = None,
) -> None:
    print(f"\n--- Starte L.A.R.A. Agent fuer Frage: '{user_query}' ---\n")

    print("Starte MCP Server Instanz und initialisiere Tools...")
    print("Lasse KI nachdenken (inkl. automatischem Retry bei Rate-Limit)...")

    result = await run_query_once(
        user_query,
        provider_override=provider_override,
        model_override=model_override,
        verbose_retry=True,
    )

    print(
        "Server meldet "
        f"{len(result['available_tools'])} verfuegbare Tools: {result['available_tools']}"
    )
    print(
        f"Lasse KI nachdenken ({result['model']} via {result['provider_label']})..."
    )

    if result["tool_calls"]:
        for tool_call in result["tool_calls"]:
            print(
                f"⚙️ KI ruft Tool auf: {tool_call['name']} "
                f"mit Argumenten: {tool_call['args']}"
            )
            print(
                f"📥 Tool hat {tool_call['result_chars']} Zeichen zurueckgeliefert. "
                "Hier ist der Anfang:"
            )
            print("-" * 40)
            print(tool_call["result_preview"])
            print("-" * 40)

        print("Lasse KI die Suchergebnisse interpretieren und finale Antwort generieren...")
        print("\n=== L.A.R.A. RESULTAT ===")
        print(result["final_answer"])
        print("=========================\n")
        return

    print("\n=== L.A.R.A. RESULTAT (Ohne Tool) ===")
    print(result["final_answer"])
    print("=====================================\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the L.A.R.A. agent.")
    parser.add_argument("--provider", choices=["gemini", "ollama"])
    parser.add_argument("--model", type=str)
    parser.add_argument("--query", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    print("======================================================")
    print("Willkommen bei L.A.R.A.")
    print("Dein Agentic-RAG Forschungs-Assistent (Gemini/Ollama).")
    print(f"Aktiver LLM Provider: {resolve_provider(args.provider)}")
    if args.model:
        print(f"Aktives Modell-Override: {args.model}")
    print("Tippe 'exit' oder 'quit' um das Programm zu beenden.")
    print("======================================================\n")

    if args.query:
        asyncio.run(
            run_agentic_loop(
                args.query,
                provider_override=args.provider,
                model_override=args.model,
            )
        )
        raise SystemExit(0)

    while True:
        user_input = input("Deine Frage an L.A.R.A.: ")

        if user_input.lower() in ["exit", "quit"]:
            print("L.A.R.A. wird beendet. Bis bald!")
            break

        if not user_input.strip():
            continue

        asyncio.run(
            run_agentic_loop(
                user_input,
                provider_override=args.provider,
                model_override=args.model,
            )
        )