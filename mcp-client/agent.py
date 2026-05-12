import asyncio
import json
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. Konfiguration für unser Plug & Play System
OLLAMA_BASE_URL = "http://localhost:11434/v1" # Ollama's OpenAI-kompatible API
MODEL_NAME = "mistral" # Das Modell, das wir in Ollama geladen haben

# Pfad zu unserem LARA TypeScript MCP Server
MCP_SERVER_SCRIPT = "../mcp-server/index.ts"

async def run_agentic_loop(user_query: str):
    print(f"\n--- Starte L.A.R.A. Agent für Frage: '{user_query}' ---\n")
    
    # 2. Verbindung zum lokalen Ollama herstellen
    llm_client = AsyncOpenAI(
        base_url=OLLAMA_BASE_URL,
        api_key="LokalBrauchenWirKeinenKey"
    )

    # 3. Verbindung zum MCP Server (TypeScript) aufbauen
    print("Starte MCP Server Instanz...")
    server_params = StdioServerParameters(
        command="npx",
        args=["tsx", MCP_SERVER_SCRIPT]
    )

    # Der stdio_client startet den TS-Server unsichtbar im Hintergrund
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            
            # Initialisiere die MCP-Session
            await session.initialize()
            
            # 4. Tools vom Server abfragen (Das "Menü" für die KI)
            tools_response = await session.list_tools()
            
            # Wir formatieren die MCP-Tools in das OpenAI-Format um, 
            # damit Mistral sie versteht.
            agent_tools = []
            for tool in tools_response.tools:
                agent_tools.append({
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })
            
            print(f"Server meldet {len(agent_tools)} verfügbare Tools: {[t['function']['name'] for t in agent_tools]}")

            # 5. Der System-Prompt: Wer ist die KI?
            messages = [
                {
                    "role": "system", 
                    "content": (
                        "Du bist L.A.R.A., ein präziser, lokaler Forschungs-Assistent. "
                        "Antworte immer auf Deutsch. Nutze dein Such-Tool, um in den "
                        "lokalen Dokumenten nach Fakten zu suchen, bevor du antwortest. "
                        "Vermeide es zu halluzinieren."
                    )
                },
                {"role": "user", "content": user_query}
            ]

            # 6. SCHLEIFE 1: KI entscheidet, ob sie ein Tool nutzen muss
            print("Lasse KI nachdenken (Mistral via Ollama)...")
            response = await llm_client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=agent_tools,
                temperature=0.1 # Niedrige Temperatur für fokussierte, faktische Antworten
            )

            response_message = response.choices[0].message
            messages.append(response_message) # Die Antwort in den Verlauf aufnehmen

            # Hat die KI entschieden, ein Tool (z.B. die ES-Suche) zu nutzen?
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    # Ollama/OpenAI liefert die Argumente als JSON-String
                    tool_args = json.loads(tool_call.function.arguments) 
                    
                    print(f"⚙️ KI ruft Tool auf: {tool_name} mit Argumenten: {tool_args}")
                    
                    # 7. TOOL AUSFÜHREN (Aufruf an den MCP Server -> Elasticsearch)
                    tool_result = await session.call_tool(tool_name, tool_args)
                    
                    # Ergebnis extrahieren (Der MCP Server liefert in der Regel Text zurück)
                    result_text = "\n".join([content.text for content in tool_result.content if content.type == "text"])
                    print(f"📥 Tool hat {len(result_text)} Zeichen zurückgeliefert.")

                    # Das Ergebnis der Suche hängen wir an den Nachrichtenverlauf an
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_text
                    })

                # 8. SCHLEIFE 2: KI fasst die neuen Informationen zusammen
                print("Lasse KI die Suchergebnisse interpretieren und finale Antwort generieren...")
                final_response = await llm_client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                )
                
                print("\n=== L.A.R.A. RESULTAT ===")
                print(final_response.choices[0].message.content)
                print("=========================\n")
            
            else:
                # KI denkt, sie kann es ohne Tool beantworten
                print("\n=== L.A.R.A. RESULTAT (Ohne Tool) ===")
                print(response_message.content)
                print("=====================================\n")

if __name__ == "__main__":
    # Test-Frage: Ersetze dies durch etwas, das wirklich in deinen Dokumenten steht!
    # z.B. "Wie funktioniert der Talentwert (TaW) im DSA 5 Regelwerk?"
    test_frage = "Kannst du mir die grundlegenden Kampfregeln in LARA zusammenfassen?"
    
    # Da die Tools asynchron sind, starten wir den asynchronen Loop
    asyncio.run(run_agentic_loop(test_frage))