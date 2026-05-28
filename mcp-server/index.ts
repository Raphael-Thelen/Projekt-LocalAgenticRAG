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
const DEFAULT_SIZE = 5;

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
        name: "search_exact_keyword",
        description:
          "Praezise keyword-basierte Suche fuer exakte Begriffe und Formulierungen.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Suchbegriff oder Query-String (z.B. Kampfregeln)",
            },
            size: {
              type: "integer",
              description: "Anzahl Treffer (Default: 5)",
              minimum: 1,
              maximum: 20,
            },
          },
          required: ["query"],
        },
      },
      {
        name: "search_phrase_proximity",
        description:
          "Phrase- und Naehe-Suche in lokalen LARA-Dokumenten (a near b).",
        inputSchema: {
          type: "object",
          properties: {
            phrase: {
              type: "string",
              description: "Exakte Phrase, falls vorhanden",
            },
            termA: {
              type: "string",
              description: "Erster Term fuer Naehe-Suche",
            },
            termB: {
              type: "string",
              description: "Zweiter Term fuer Naehe-Suche",
            },
            slop: {
              type: "integer",
              description: "Maximaler Wortabstand bei Naehe-Suche (Default: 5)",
              minimum: 0,
              maximum: 50,
            },
            size: {
              type: "integer",
              description: "Anzahl Treffer (Default: 5)",
              minimum: 1,
              maximum: 20,
            },
          },
          oneOf: [{ required: ["phrase"] }, { required: ["termA", "termB"] }],
        },
      },
      {
        name: "search_fuzzy",
        description:
          "Robuste Suche fuer Tippfehler, Wortvarianten und unscharfe Formulierungen.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Suchbegriff mit toleranter Trefferlogik",
            },
            size: {
              type: "integer",
              description: "Anzahl Treffer (Default: 5)",
              minimum: 1,
              maximum: 20,
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

type ToolDocResult = {
  source: string;
  title: string;
  page: number | null;
  score: number | null;
  chunk_id: string;
  doc_id: string;
  excerpt: string;
};

function clampSize(rawSize: unknown): number {
  const parsed = Number(rawSize);
  if (!Number.isFinite(parsed)) {
    return DEFAULT_SIZE;
  }

  return Math.min(20, Math.max(1, Math.floor(parsed)));
}

function normalizeHit(hit: any): ToolDocResult {
  const source = hit?._source ?? {};

  return {
    source: String(source.source ?? "unknown"),
    title: String(source.title ?? source.source ?? "unknown"),
    page: typeof source.page === "number" ? source.page : null,
    score: typeof hit?._score === "number" ? hit._score : null,
    chunk_id: String(source.chunk_id ?? hit?._id ?? "unknown"),
    doc_id: String(source.doc_id ?? source.source ?? "unknown"),
    excerpt: String(source.content ?? "").slice(0, 1200),
  };
}

function toMcpTextResult(
  tool: string,
  queryInfo: Record<string, unknown>,
  hits: any[],
) {
  const normalized = hits.map(normalizeHit);

  return {
    tool,
    index: INDEX_NAME,
    query: queryInfo,
    count: normalized.length,
    results: normalized,
  };
}

// 5. Tool-Logik implementieren (Was passiert, wenn das LLM das Tool aufruft?)
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const toolName = request.params.name;
  const args = request.params.arguments ?? {};

  try {
    if (toolName === "search_exact_keyword") {
      const query = String(args.query ?? "").trim();
      const size = clampSize(args.size);

      if (!query) {
        throw new Error("'query' ist fuer search_exact_keyword erforderlich.");
      }

      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: {
            bool: {
              should: [
                {
                  simple_query_string: {
                    query,
                    fields: ["content", "title^2"],
                    default_operator: "and",
                  },
                },
                {
                  match_phrase: {
                    content: {
                      query,
                      slop: 1,
                      boost: 2,
                    },
                  },
                },
              ],
              minimum_should_match: 1,
            },
          },
          size,
        },
      });

      const payload = toMcpTextResult(toolName, { query, size }, hits.hits);
      return {
        content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
      };
    }

    if (toolName === "search_phrase_proximity") {
      const phrase = String(args.phrase ?? "").trim();
      const termA = String(args.termA ?? "").trim();
      const termB = String(args.termB ?? "").trim();
      const slop = Number.isFinite(Number(args.slop))
        ? Math.max(0, Math.min(50, Math.floor(Number(args.slop))))
        : 5;
      const size = clampSize(args.size);

      if (!phrase && (!termA || !termB)) {
        throw new Error(
          "Bitte entweder 'phrase' oder beide Felder 'termA' und 'termB' angeben.",
        );
      }

      const queryBody = phrase
        ? {
            match_phrase: {
              content: {
                query: phrase,
                slop,
              },
            },
          }
        : {
            span_near: {
              clauses: [
                {
                  span_term: {
                    content: termA,
                  },
                },
                {
                  span_term: {
                    content: termB,
                  },
                },
              ],
              slop,
              in_order: false,
            },
          };

      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: queryBody,
          size,
        },
      });

      const payload = toMcpTextResult(
        toolName,
        phrase ? { phrase, slop, size } : { termA, termB, slop, size },
        hits.hits,
      );
      return {
        content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
      };
    }

    if (toolName === "search_fuzzy") {
      const query = String(args.query ?? "").trim();
      const size = clampSize(args.size);

      if (!query) {
        throw new Error("'query' ist fuer search_fuzzy erforderlich.");
      }

      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: {
            bool: {
              should: [
                {
                  multi_match: {
                    query,
                    fields: ["content", "title^2"],
                    fuzziness: "AUTO",
                    operator: "and",
                    prefix_length: 1,
                  },
                },
                {
                  match: {
                    content: {
                      query,
                      fuzziness: "AUTO",
                      operator: "or",
                      boost: 0.7,
                    },
                  },
                },
                {
                  match_phrase_prefix: {
                    content: {
                      query,
                      max_expansions: 50,
                      boost: 0.6,
                    },
                  },
                },
              ],
              minimum_should_match: 1,
            },
          },
          size,
        },
      });

      const payload = toMcpTextResult(toolName, { query, size }, hits.hits);
      return {
        content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
      };
    }

    throw new Error(`Tool '${toolName}' nicht gefunden.`);
  } catch (error: any) {
    return {
      content: [
        {
          type: "text",
          text: `Elasticsearch/Tool Fehler: ${error.message}`,
        },
      ],
      isError: true,
    };
  }
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
