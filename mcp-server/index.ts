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
      {
        name: "search_smart",
        description:
          "LLM-geplanter Retrieval-Flow: natuerliche Frage -> validierter Suchplan -> ES Query mit Fallback.",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "Natuerliche Nutzerfrage",
            },
            size: {
              type: "integer",
              description: "Anzahl Treffer (Default: 5)",
              minimum: 1,
              maximum: 20,
            },
            plan: {
              type: "object",
              description: "Optional vorgeplanter Smart-Plan vom Client-LLM.",
            },
            planner_source: {
              type: "string",
              description: "Optionales Source-Label fuer den vorgeplanten Plan.",
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

type SmartRetrievalMode = "fuzzy_only" | "fuzzy_plus_exact" | "balanced";

type SmartQueryPlan = {
  normalized_query: string;
  keyword_terms: string[];
  expanded_terms: string[];
  retrieval_mode: SmartRetrievalMode;
  top_k: number;
  confidence: number;
  rationale: string;
};

const SMART_DOMAIN_HINTS = [
  "Domain ist DSA/Aventurien-Regelwerk und Lore.",
  "Behandle Umlaute und ASCII-Varianten als gleichwertig (zwoelfgoetter/zwölfgötter, fuer/für).",
  "Nutze regelnahe Fachanker in keyword_terms, z.B. Fertigkeitsprobe, FW, FP, QS, Patzer, Bestaetigungswurf, Schicksalspunkt, LE, SK, ZK, GS, Arcanovi.",
  "Bei konkreten Regelmechaniken oder Zahlenfragen retrieval_mode=fuzzy_plus_exact bevorzugen.",
  "Bei sehr offenen Beschreibungsfragen retrieval_mode=balanced erlauben.",
  "expanded_terms fuer Synonyme und Schreibvarianten nutzen, aber keine Halluzinationsbegriffe erfinden.",
];

const REWRITE_STOPWORDS = new Set([
  "ab",
  "als",
  "am",
  "an",
  "auch",
  "aus",
  "bei",
  "bis",
  "das",
  "dass",
  "dem",
  "den",
  "der",
  "des",
  "die",
  "ein",
  "eine",
  "einem",
  "einen",
  "einer",
  "er",
  "es",
  "fuer",
  "für",
  "gilt",
  "hat",
  "heisst",
  "heißt",
  "im",
  "in",
  "ist",
  "mit",
  "nach",
  "oder",
  "sich",
  "sind",
  "und",
  "von",
  "wann",
  "warum",
  "was",
  "welche",
  "welchem",
  "welchen",
  "welcher",
  "welches",
  "wer",
  "wie",
  "wird",
  "wurde",
  "zu",
]);

const REWRITE_EXPANSIONS: Record<string, string[]> = {
  schicksalspunkt: ["schicksalspunkte", "schip"],
  schicksalspunkte: ["schicksalspunkt", "schips"],
  zwoelfgoetter: ["zwölfgötter", "zwolfgotter"],
  zwolfgoetter: ["zwölfgötter", "zwoelfgoetter"],
  bestaetigungswurf: ["bestätigungswurf"],
  fertigkeitswert: ["fw", "fertigkeitsprobe", "fp", "qs"],
  fertigkeitsprobe: ["3w20", "fertigkeitswert", "fw", "fp", "qs"],
};

function clampSize(rawSize: unknown): number {
  const parsed = Number(rawSize);
  if (!Number.isFinite(parsed)) {
    return DEFAULT_SIZE;
  }

  return Math.min(20, Math.max(1, Math.floor(parsed)));
}

function tokenizeForRewrite(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[.,!?;:()\[\]{}"'`´_\-\/\\|]+/g, " ")
    .split(/\s+/)
    .filter(Boolean);
}

function collectRewriteTerms(text: string): string[] {
  const tokens = tokenizeForRewrite(text);
  const out: string[] = [];
  const seen = new Set<string>();

  for (const token of tokens) {
    if (REWRITE_STOPWORDS.has(token)) {
      continue;
    }

    const keep = token.length >= 3 || /^\d+[a-z]*$/i.test(token);
    if (!keep) {
      continue;
    }

    if (!seen.has(token)) {
      out.push(token);
      seen.add(token);
    }

    const expansions = REWRITE_EXPANSIONS[token] ?? [];
    for (const expanded of expansions) {
      if (!seen.has(expanded)) {
        out.push(expanded);
        seen.add(expanded);
      }
    }
  }

  return out;
}

function rewriteExactQuery(query: string): string {
  const terms = collectRewriteTerms(query);
  return terms.slice(0, 10).join(" ").trim();
}

function rewriteExactTerms(query: string): string[] {
  return collectRewriteTerms(query).slice(0, 10);
}

function buildExactShouldClauses(rawQuery: string, rewrittenTerms: string[]): any[] {
  const rewrittenQuery = rewrittenTerms.join(" ");
  const rewrittenOrQuery = rewrittenTerms.join(" | ");
  const minimumShouldMatch = minimumShouldMatchForTerms(rewrittenTerms.length);

  const shouldClauses: any[] = [
    {
      simple_query_string: {
        query: rawQuery,
        fields: ["content", "title^2"],
        default_operator: "and",
        boost: 0.5,
      },
    },
  ];

  if (!rewrittenQuery) {
    return shouldClauses;
  }

  shouldClauses.push(
    {
      simple_query_string: {
        query: rewrittenQuery,
        fields: ["content", "title^2"],
        default_operator: "and",
        boost: 1.5,
      },
    },
    {
      simple_query_string: {
        query: rewrittenOrQuery,
        fields: ["content", "title^2"],
        default_operator: "or",
        minimum_should_match: minimumShouldMatch,
        boost: 1.3,
      },
    },
    {
      match: {
        content: {
          query: rewrittenQuery,
          operator: "and",
          boost: 1.0,
        },
      },
    },
    {
      multi_match: {
        query: rewrittenQuery,
        fields: ["content", "title^2"],
        operator: "or",
        minimum_should_match: minimumShouldMatch,
        boost: 1.1,
      },
    },
    {
      match_phrase: {
        content: {
          query: rewrittenQuery,
          slop: 2,
          boost: 1.2,
        },
      },
    },
  );

  return shouldClauses;
}

function buildFuzzyShouldClauses(query: string): any[] {
  return [
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
  ];
}

function parseStringArray(value: unknown): string[] {
  if (!Array.isArray(value)) {
    return [];
  }

  return value
    .map((entry) => String(entry ?? "").trim().toLowerCase())
    .filter(Boolean)
    .slice(0, 12);
}

function parseSmartPlan(candidate: unknown, fallbackTopK: number): SmartQueryPlan | null {
  if (!candidate || typeof candidate !== "object") {
    return null;
  }

  const obj = candidate as Record<string, unknown>;
  const normalizedQuery = String(obj.normalized_query ?? "").trim();
  const keywordTerms = parseStringArray(obj.keyword_terms);
  const expandedTerms = parseStringArray(obj.expanded_terms);
  const retrievalModeRaw = String(obj.retrieval_mode ?? "").trim();
  const topK = clampSize(obj.top_k ?? fallbackTopK);
  const confidenceRaw = Number(obj.confidence);
  const rationale = String(obj.rationale ?? "").trim().slice(0, 300);

  const retrievalMode: SmartRetrievalMode = (
    retrievalModeRaw === "fuzzy_only" ||
    retrievalModeRaw === "fuzzy_plus_exact" ||
    retrievalModeRaw === "balanced"
  )
    ? retrievalModeRaw
    : "fuzzy_plus_exact";

  if (!normalizedQuery) {
    return null;
  }

  const confidence = Number.isFinite(confidenceRaw)
    ? Math.min(1, Math.max(0, confidenceRaw))
    : 0.5;

  return {
    normalized_query: normalizedQuery,
    keyword_terms: keywordTerms,
    expanded_terms: expandedTerms,
    retrieval_mode: retrievalMode,
    top_k: topK,
    confidence,
    rationale: rationale || "n/a",
  };
}

function buildHeuristicSmartPlan(query: string, size: number): SmartQueryPlan {
  const rewrittenTerms = rewriteExactTerms(query);
  const hasQuotedPhrase = /"[^"]+"/.test(query);
  const hasDigits = /\d/.test(query);

  const retrievalMode: SmartRetrievalMode =
    hasQuotedPhrase || hasDigits || rewrittenTerms.length >= 3
      ? "fuzzy_plus_exact"
      : "fuzzy_only";

  return {
    normalized_query: query.trim(),
    keyword_terms: rewrittenTerms.slice(0, 6),
    expanded_terms: rewrittenTerms.slice(0, 10),
    retrieval_mode: retrievalMode,
    top_k: size,
    confidence: 0.45,
    rationale: "heuristic_fallback",
  };
}

function extractFirstJsonObject(text: string): string | null {
  const start = text.indexOf("{");
  if (start < 0) {
    return null;
  }

  let depth = 0;
  for (let i = start; i < text.length; i += 1) {
    const ch = text[i];
    if (ch === "{") {
      depth += 1;
    } else if (ch === "}") {
      depth -= 1;
      if (depth === 0) {
        return text.slice(start, i + 1);
      }
    }
  }

  return null;
}

async function buildSmartPlan(query: string, size: number): Promise<{
  plan: SmartQueryPlan;
  planner_source: "ollama" | "heuristic";
}> {
  const fallback = buildHeuristicSmartPlan(query, size);
  const ollamaBaseUrl = String(process.env.OLLAMA_BASE_URL ?? "").trim();
  const ollamaModel = String(process.env.OLLAMA_MODEL_NAME ?? "llama3.1").trim();
  const plannerTimeoutMsRaw = Number(process.env.LARA_SMART_PLANNER_TIMEOUT_MS ?? 2500);
  const plannerTimeoutMs = Number.isFinite(plannerTimeoutMsRaw)
    ? Math.max(200, Math.floor(plannerTimeoutMsRaw))
    : 2500;

  if (!ollamaBaseUrl) {
    return { plan: fallback, planner_source: "heuristic" };
  }

  const plannerPrompt = [
    "You are a query planner for an Elasticsearch retrieval stack.",
    "Return only valid JSON with exactly these keys and no additional keys:",
    "normalized_query (string), keyword_terms (string[]), expanded_terms (string[]), retrieval_mode (fuzzy_only|fuzzy_plus_exact|balanced), top_k (integer), confidence (0..1), rationale (string).",
    "keyword_terms: precise retrieval anchors, ideally 2-6 terms.",
    "expanded_terms: spelling variants/synonyms for broader recall, ideally 3-10 terms.",
    "Do not include punctuation-heavy or sentence-like entries in keyword_terms/expanded_terms.",
    "If uncertain, pick fuzzy_plus_exact instead of fuzzy_only.",
    "Domain hints:",
    ...SMART_DOMAIN_HINTS.map((hint) => `- ${hint}`),
    `User query: ${query}`,
    `Requested top_k: ${size}`,
  ].join("\n");

  let plannerEndpoint = ollamaBaseUrl.replace(/\/$/, "");
  if (plannerEndpoint.endsWith("/v1")) {
    plannerEndpoint = plannerEndpoint.slice(0, -3);
  }
  plannerEndpoint = `${plannerEndpoint}/api/generate`;

  const abortController = new AbortController();
  const timeoutHandle = setTimeout(() => {
    abortController.abort();
  }, plannerTimeoutMs);

  try {
    const response = await fetch(plannerEndpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      signal: abortController.signal,
      body: JSON.stringify({
        model: ollamaModel,
        prompt: plannerPrompt,
        stream: false,
        format: "json",
      }),
    });

    clearTimeout(timeoutHandle);

    if (!response.ok) {
      return { plan: fallback, planner_source: "heuristic" };
    }

    const data = await response.json() as { response?: string };
    const text = String(data.response ?? "");
    const jsonText = extractFirstJsonObject(text) ?? text;

    let parsed: unknown;
    try {
      parsed = JSON.parse(jsonText);
    } catch {
      return { plan: fallback, planner_source: "heuristic" };
    }

    const validated = parseSmartPlan(parsed, size);
    if (!validated) {
      return { plan: fallback, planner_source: "heuristic" };
    }

    return {
      plan: validated,
      planner_source: "ollama",
    };
  } catch {
    clearTimeout(timeoutHandle);
    return { plan: fallback, planner_source: "heuristic" };
  }
}

function compileSmartShouldClauses(rawQuery: string, plan: SmartQueryPlan): any[] {
  const normalized = plan.normalized_query || rawQuery;
  const expandedQuery = [
    normalized,
    ...plan.expanded_terms,
  ].join(" ").trim();

  const fuzzyClauses = buildFuzzyShouldClauses(expandedQuery || normalized);
  if (plan.retrieval_mode === "fuzzy_only") {
    return fuzzyClauses;
  }

  const exactSeed = plan.keyword_terms.length
    ? plan.keyword_terms
    : rewriteExactTerms(rawQuery);
  const exactClauses = buildExactShouldClauses(normalized || rawQuery, exactSeed);

  if (plan.retrieval_mode === "balanced") {
    return [...fuzzyClauses, ...exactClauses];
  }

  return [
    ...fuzzyClauses,
    ...exactClauses.map((clause) => {
      if (clause.simple_query_string?.boost) {
        return {
          simple_query_string: {
            ...clause.simple_query_string,
            boost: Number(clause.simple_query_string.boost) * 1.15,
          },
        };
      }
      return clause;
    }),
  ];
}

function minimumShouldMatchForTerms(termCount: number): string {
  if (termCount <= 2) {
    return "100%";
  }
  if (termCount <= 4) {
    return "75%";
  }
  return "60%";
}

function rewriteProximityInput(phrase: string): {
  rewrittenPhrase: string;
  nearTerms: [string, string] | null;
} {
  const terms = collectRewriteTerms(phrase);
  const rewrittenPhrase = terms.slice(0, 6).join(" ").trim();

  if (terms.length >= 2) {
    return {
      rewrittenPhrase,
      nearTerms: [terms[0], terms[1]],
    };
  }

  return {
    rewrittenPhrase,
    nearTerms: null,
  };
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
      const rewrittenTerms = rewriteExactTerms(query);
      const rewrittenQuery = rewrittenTerms.join(" ");
      const rewrittenOrQuery = rewrittenTerms.join(" | ");
      const minimumShouldMatch = minimumShouldMatchForTerms(rewrittenTerms.length);

      if (!query) {
        throw new Error("'query' ist fuer search_exact_keyword erforderlich.");
      }

      const shouldClauses: any[] = [
        {
          simple_query_string: {
            query,
            fields: ["content", "title^2"],
            default_operator: "and",
            boost: 0.5,
          },
        },
      ];

      if (rewrittenQuery) {
        shouldClauses.push(
          {
            simple_query_string: {
              query: rewrittenQuery,
              fields: ["content", "title^2"],
              default_operator: "and",
              boost: 1.5,
            },
          },
          {
            simple_query_string: {
              query: rewrittenOrQuery,
              fields: ["content", "title^2"],
              default_operator: "or",
              minimum_should_match: minimumShouldMatch,
              boost: 1.3,
            },
          },
          {
            match: {
              content: {
                query: rewrittenQuery,
                operator: "and",
                boost: 1.0,
              },
            },
          },
          {
            multi_match: {
              query: rewrittenQuery,
              fields: ["content", "title^2"],
              operator: "or",
              minimum_should_match: minimumShouldMatch,
              boost: 1.1,
            },
          },
          {
            match_phrase: {
              content: {
                query: rewrittenQuery,
                slop: 2,
                boost: 1.2,
              },
            },
          },
        );
      }

      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: {
            bool: {
              should: shouldClauses,
              minimum_should_match: 1,
            },
          },
          size,
        },
      });

      const payload = toMcpTextResult(
        toolName,
        {
          query,
          rewritten_query: rewrittenQuery || null,
          rewritten_or_query: rewrittenOrQuery || null,
          minimum_should_match: rewrittenQuery ? minimumShouldMatch : null,
          size,
        },
        hits.hits,
      );
      return {
        content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
      };
    }

    if (toolName === "search_phrase_proximity") {
      const phrase = String(args.phrase ?? "").trim();
      const termA = String(args.termA ?? "").trim().toLowerCase();
      const termB = String(args.termB ?? "").trim().toLowerCase();
      const slop = Number.isFinite(Number(args.slop))
        ? Math.max(0, Math.min(50, Math.floor(Number(args.slop))))
        : 5;
      const size = clampSize(args.size);

      if (!phrase && (!termA || !termB)) {
        throw new Error(
          "Bitte entweder 'phrase' oder beide Felder 'termA' und 'termB' angeben.",
        );
      }

      const rewritten = rewriteProximityInput(phrase);
      const nearTerms: [string, string] | null = termA && termB
        ? [termA, termB]
        : rewritten.nearTerms;

      const shouldClauses: any[] = [];

      if (phrase) {
        shouldClauses.push({
          match_phrase: {
            content: {
              query: phrase,
              slop,
              boost: 0.6,
            },
          },
        });
      }

      if (rewritten.rewrittenPhrase) {
        shouldClauses.push({
          match_phrase: {
            content: {
              query: rewritten.rewrittenPhrase,
              slop,
              boost: 1.2,
            },
          },
        });
      }

      if (nearTerms) {
        shouldClauses.push({
          span_near: {
            clauses: [
              {
                span_term: {
                  content: nearTerms[0],
                },
              },
              {
                span_term: {
                  content: nearTerms[1],
                },
              },
            ],
            slop,
            in_order: false,
          },
        });
      }

      if (!shouldClauses.length) {
        throw new Error("Konnte keine gueltige Proximity-Query erzeugen.");
      }

      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: {
            bool: {
              should: shouldClauses,
              minimum_should_match: 1,
            },
          },
          size,
        },
      });

      const payload = toMcpTextResult(
        toolName,
        {
          phrase: phrase || null,
          rewritten_phrase: rewritten.rewrittenPhrase || null,
          termA: nearTerms?.[0] ?? null,
          termB: nearTerms?.[1] ?? null,
          slop,
          size,
        },
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

    if (toolName === "search_smart") {
      const query = String(args.query ?? "").trim();
      const size = clampSize(args.size);

      if (!query) {
        throw new Error("'query' ist fuer search_smart erforderlich.");
      }

      const providedPlan = parseSmartPlan(args.plan, size);
      const providedPlannerSource = String(args.planner_source ?? "").trim();

      const { plan, planner_source } = providedPlan
        ? {
          plan: providedPlan,
          planner_source: (providedPlannerSource || "client").toLowerCase(),
        }
        : await buildSmartPlan(query, size);

      const shouldClauses = compileSmartShouldClauses(query, plan);

      const { hits } = await esClient.search({
        index: INDEX_NAME,
        body: {
          query: {
            bool: {
              should: shouldClauses,
              minimum_should_match: 1,
            },
          },
          size: plan.top_k,
        },
      });

      const payload = toMcpTextResult(
        toolName,
        {
          query,
          planner_source,
          plan,
          compiled_should_clauses: shouldClauses.length,
        },
        hits.hits,
      );
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
