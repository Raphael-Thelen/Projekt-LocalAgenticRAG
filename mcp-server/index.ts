import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { Client } from "@elastic/elasticsearch";

// 1. Konfiguration
const ES_HOST = "http://localhost:9200";
const INDEX_NAME = "lara_documents";

// 2. Elasticsearch Client initialisieren
const esClient = new Client({ node: ES_HOST });

// 3. MCP Server initialisieren
const server = new Server(
  {
    name: "lara-search-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {}, // Wir sagen dem Client: Dieser Server bietet Tools an
    },
  },
);

// 4. Tools definieren (Das ist das "Menü" für das LLM)
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_lara_documents",
        description:
          "Sucht nach semantischen Informationen in den lokalen " +
          "LARA-Dokumenten (Regelwerke und Hintergrundwissen).",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description:
                "Der Suchbegriff oder die Frage (z.B. 'Kampfregeln')",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

// 5. Tool-Logik implementieren (Was passiert, wenn das LLM das Tool aufruft?)
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "search_lara_documents") {
    // LLMs übergeben Parameter als beliebiges Objekt, wir casten es sicher
    const query = String(request.params.arguments?.query || "");

    if (!query) {
      throw new Error("Fehler: 'query' Argument ist zwingend erforderlich.");
    }

    try {
      // Elasticsearch Abfrage (Multi-Match auf den Inhalt)
      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: {
            multi_match: {
              query: query,
              fields: ["content"],
              fuzziness: "AUTO", // Erlaubt kleine Tippfehler bei der Suche
            },
          },
          size: 5, // Gib die Top 5 Text-Chunks zurück
        },
      });

      // Ergebnisse formatieren
      const results = hits.hits.map((hit: any) => {
        const source = hit._source;
        return `Dokument: ${source.source} (Seite ${source.page})\n${source.content}`;
      });

      const responseText = results.length
        ? results.join("\n\n---\n\n")
        : "Keine treffenden Informationen in LARA gefunden.";

      // MCP Tool Result zurückgeben
      return {
        content: [
          {
            type: "text",
            text: responseText,
          },
        ],
      };
    } catch (error: any) {
      return {
        content: [
          {
            type: "text",
            text: `Elasticsearch Fehler: ${error.message}`,
          },
        ],
        isError: true,
      };
    }
  }

  throw new Error("Tool nicht gefunden");
});

// 6. Server starten (Kommunikation über Standard Input/Output)
async function run() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("LARA MCP Server läuft (Stdio Transport).");
}

run().catch((error) => {
  console.error("Fataler Fehler im Server:", error);
  process.exit(1);
});
