# Implementing Hybrid Retrieval Log

Dieses Dokument protokolliert alle Arbeitsschritte zur Implementierung von `search_semantic` und den zugehoerigen Anpassungen.

## 2026-07-09 - Start

- Aufgabe aufgenommen: Hybrid-/Semantic-Erweiterung end-to-end umsetzen.
- Geplante Teilaufgaben:
  - Ingestion um Vektor-Embeddings erweitern.
  - MCP-Tool `search_semantic` implementieren.
  - Testbench um `search_semantic` erweitern.
  - Neuen Testlauf ausfuehren und Artefakte dokumentieren.
- Kontext geprueft:
  - Aktuelles Mapping ist textbasiert ohne Vector-Felder.
  - Aktuelle MCP-Tools: `search_exact_keyword`, `search_phrase_proximity`, `search_fuzzy`, `search_smart`.
  - Testbench kennt diese 4 Tools bereits.

## Laufendes Protokoll

- [abgeschlossen] Ingestion erweitert in [ingestion/ingest.py](ingestion/ingest.py):
  - Neue CLI-Optionen fuer Vektor-Ingestion hinzugefuegt:
    - `--enable-vectors`
    - `--embedding-model`
    - `--embedding-api-url`
    - `--embedding-dims`
    - `--embedding-timeout`
    - `--embedding-fail-fast`
  - Neue Klasse `OllamaEmbedder` implementiert (HTTP POST auf `/api/embeddings`).
  - Mapping-Erweiterung bei aktivierten Vektoren: Feld `content_vector` als `dense_vector` mit konfigurierbarer `dims`.
  - Chunk-Ingestion schreibt pro Chunk optional `content_vector`.
  - Robustes Verhalten bei Embedding-Fehlern: Warnung + Indexierung ohne Vektor (oder Abbruch bei `--embedding-fail-fast`).
  - Dimensions-Probe eingebaut (`--embedding-dims 0` => automatische Erkennung).

- [abgeschlossen] MCP-Tool `search_semantic` erweitert in [mcp-server/index.ts](mcp-server/index.ts):
  - Neues Tool `search_semantic` im Tool-Menue registriert.
  - Parameter:
    - `query` (required)
    - `size` (optional)
    - `mode` (`semantic_only` oder `hybrid`, default `hybrid`)
  - Embedding-Aufbau ueber Ollama (`OLLAMA_BASE_URL` + `/api/embeddings`) implementiert.
  - Bei erfolgreichem Embedding:
    - semantische Scoring-Klausel via `script_score` + `cosineSimilarity` auf `content_vector`.
    - in `hybrid` zusaetzlich fuzzy-basierte lexikale Should-Klauseln.
  - Bei Embedding-Fehlern oder fehlender Ollama-Konfiguration:
    - automatischer lexicaler Fallback (`search_fuzzy`-artige Klauseln), damit der Tool-Call nicht hart fehlschlaegt.

- [abgeschlossen] Testbench erweitert:
  - [experiments/run_testbench.py](experiments/run_testbench.py):
    - `search_semantic` in `TOOLS` aufgenommen.
    - Arg-Builder fuer `user`, `realistic_args`, `smart_args` und diagnostischen Fallback auf `query`-basierte Args erweitert.
  - [experiments/testbench-v1.json](experiments/testbench-v1.json):
    - Toolliste um `search_semantic` erweitert.
    - Beschreibung auf `10 Fragen x 5 Retrieval-Tools` angepasst.

- [in Arbeit] Nächster Schritt: neuen Testlauf ausfuehren und Artefakte dokumentieren.

## 2026-07-09 - Ausfuehrung und Verifikation

- [abgeschlossen] Vektor-Ingestion erfolgreich ausgefuehrt:
  - Kommando:
    - `/Users/raphaelthelen/Arbeitsplatz/Uni/Projekt-LocalAgenticRAG/.venv/bin/python ingestion/ingest.py --reset-index --glob 'Regelwerk.pdf' --enable-vectors --embedding-model nomic-embed-text --embedding-api-url http://127.0.0.1:11434/api/embeddings --embedding-timeout 60 --embedding-fail-fast`
  - Ergebnis:
    - `regelwerk: 2077 Chunks`
    - `Indexiert: 2077, Fehler: 0`
  - Mapping-Verifikation:
    - Index `lara_documents` enthaelt `content_vector` als `dense_vector` mit `dims: 768`.

- [abgeschlossen] Neuer Testrun mit `search_semantic` und Gemini-API:
  - Kommando:
    - `OLLAMA_BASE_URL=http://127.0.0.1:11434/v1 LARA_EMBED_MODEL=nomic-embed-text /Users/raphaelthelen/Arbeitsplatz/Uni/Projekt-LocalAgenticRAG/.venv/bin/python experiments/run_testbench.py --spec experiments/testbench-smoke-q1.json --tools search_semantic --modes user --provider gemini --run-group session-5-hybrid-semantic`
  - Artefakte:
    - `experiments/runs/5 - Hybrid Smoke Test/20260709-101921-user/run-user.json`
    - `experiments/runs/5 - Hybrid Smoke Test/20260709-101921-user/manual-review-user.txt`
    - `experiments/runs/5 - Hybrid Smoke Test/20260709-101921-user/score-user.json`
    - `experiments/runs/5 - Hybrid Smoke Test/20260709-101921-user/score-summary-user.txt`
  - Laufzusammenfassung:
    - Retrieval: 5 Treffer
    - Antwort (erste Zeile): "Das Mittelreich wird von Kaiserin Rohaja regiert. Die Hauptstadt des Mittelreichs ist Gareth."
    - Antwortbewertung: 1/1 korrekt (C); Strict Precision, Lenient Recall und gewichteter Antwortscore jeweils 1.000.
    - Retrieval-Metriken: Macro-Precision 0.200, Macro-Recall 1.000, Hit-Rate 1.000. Der gespeicherte Lauf nutzte den lexikalen Fallback (`semantic_status: fallback_lexical`).

- [dokumentiert] Troubleshooting-Hinweis waehrend der Implementierung:
  - Ein erster Testlauf mit `--provider ollama` schlug in der LLM-Schicht mit `404 page not found` fehl.
  - Ursache: falscher Ollama-Base-Endpoint fuer OpenAI-kompatible Chat-Calls (fehlendes `/v1`).
  - Loesung: fuer LLM-Calls `OLLAMA_BASE_URL=http://127.0.0.1:11434/v1`; fuer Embeddings wird im MCP-Server intern auf `/api/embeddings` normalisiert.

- [abgeschlossen] Robustheitsfix fuer Embedding-Aufbau im MCP-Server:
  - Datei: `mcp-server/index.ts`
  - Aenderung: `buildQueryEmbedding` nutzt nun default `http://127.0.0.1:11434`, falls `OLLAMA_BASE_URL` nicht gesetzt ist.
  - Ziel: `search_semantic` faellt nicht mehr allein wegen fehlender Env-Var auf lexical fallback zurueck.

- [abgeschlossen] Finaler Evaluationslauf mit Gemini (wie gewuenscht):
  - Kommando:
    - `/Users/raphaelthelen/Arbeitsplatz/Uni/Projekt-LocalAgenticRAG/.venv/bin/python experiments/run_testbench.py --spec experiments/testbench-smoke-q1.json --tools search_semantic --modes user --provider gemini --run-group session-5-hybrid-semantic`
  - Artefakte:
    - `experiments/runs/session-5-hybrid-semantic/20260709-102115-user/run-user.json`
    - `experiments/runs/session-5-hybrid-semantic/20260709-102115-user/manual-review-user.txt`
  - Verifikation im Run-JSON:
    - `retrieved_count: 5`
    - `semantic_status: active`
    - `embedding_source: ollama:nomic-embed-text`
