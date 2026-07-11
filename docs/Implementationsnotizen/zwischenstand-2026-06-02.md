# Zwischenstand LARA (Stand 2026-06-02)

## 1) Kurzfazit

In den letzten Tagen wurde der Evaluations- und Retrieval-Stack von einem Einzel-PDF-Prototyp auf einen vergleichbaren Multi-Run-Benchmark mit reproduzierbaren Artefakten weiterentwickelt. Der wichtigste quantitative Fortschritt ist die deutliche Verbesserung von `search_exact_keyword` bei unveraendert starker `search_fuzzy`-Performance.

Kernaussage aus den aktuellen, manuell bewerteten Runs:
- Exact wurde deutlich besser (Hit Rate je nach Modus +0.3 bis +0.5).
- Fuzzy ist stabil geblieben (kein Rueckschritt).
- Proximity ist aktuell weitgehend stabil, ohne neue Zugewinne.

## 2) Grundlage und Zielbild

Projektziel: lokales/privatsphaerisches Agentic-RAG mit MCP-Tools auf Elasticsearch fuer PDF-Wissensbestaende.

Aktuelle Systemgrundlagen:
- Elasticsearch Index: `lara_documents`
- MCP-Tools: `search_exact_keyword`, `search_phrase_proximity`, `search_fuzzy`
- Ingestion: rekursive PDF-Verarbeitung mit Chunking und Metadaten (`doc_id`, `chunk_id`, `page`, `file_path`)
- Benchmark: 10-Fragen-Testbench mit drei Modi (`realistic_args`, `user`, `diagnostic_args`)
- Bewertung: getrennte Retrieval-Metrik und manuelle Antwortqualitaet (`C/P/W`)

Relevante Implementierungsdateien:
- `ingestion/ingest.py`
- `mcp-server/index.ts`
- `experiments/run_testbench.py`
- `experiments/score_testbench.py`
- `experiments/testbench-v1.json`

## 3) Was wurde in den letzten Tagen konkret verbessert

### 3.1 Ingestion und Datenbasis
- Umbau von statischer Einzeldatei-Ingestion auf rekursive Multi-PDF-Ingestion.
- Neue Optionen fuer robusten Betrieb:
  - `--reset-index` (kompletter Neuaufbau)
  - `--replace-doc` (inkrementelles Ersetzen pro Dokument)
  - konfigurierbares Chunking (`--chunk-size`, `--chunk-overlap`)
- Behebung des Page-Mapping-Problems (vorher vielfach Seite 1):
  - Nutzung von `metadata.page_number` mit Legacy-Fallback.
- Aufnahme von `file_path` ins Mapping zur besseren Nachvollziehbarkeit von Chunk-Herkunft.

### 3.2 Benchmark-Workflow und Vergleichbarkeit
- Umstellung auf geteilte Goldtruth je Frage (`chunk_goldtruth.shared.expected_chunk_ids`) statt Tool-spezifischer Duplikate.
- Runner-Pfade auf die neue Struktur (`experiments/...`) angepasst.
- Run-Artefakte standardisiert pro Laufordner:
  - `run-<mode>.json`
  - `manual-review-<mode>.txt`
  - `score-<mode>.json`
  - `score-summary-<mode>.txt`

### 3.3 MCP Tool-Qualitaet
- Query-Rewrite in die Tools selbst verlagert (statt Testbench-seitig), damit Verhalten produktionsnah ist.
- Exact-Suche erweitert um:
  - Rewrite-Term-Extraktion inkl. Synonym/Varianz-Erweiterung
  - Kombination aus AND-/OR-Strategien
  - dynamisches `minimum_should_match`
  - zusaetzliche `match`, `multi_match`, `match_phrase`-Signale
- Proximity um Rewrite-gestuetzte Phrase-/Near-Varianten erweitert.

## 4) Report-Erzeugung per Script (heute ausgefuehrt)

Alle vorhandenen Run-Ordner mit manueller Bewertung wurden erneut gescored.

Ausgefuehrt wurde faktisch der folgende Ablauf (automatisiert ueber alle Paare `run-*.json` + `manual-review-*.txt`):

```bash
.venv/bin/python experiments/score_testbench.py --run-json <run-json> --review-txt <manual-review>
```

Ergebnis: Score-Dateien fuer 10 bewertete Runs frisch erzeugt/aktualisiert.

## 5) Gesamtergebnis ueber alle vorhandenen Runs

Hinweis: Es gibt 11 Score-Dateien im Repo. Zwei davon sind Sonderfaelle aus der Goldtruth-Aufbauphase (ein Lauf ohne Retrieval-Eval, ein Lauf ohne manuelle Ratings).

| Kohorte | Run ID | Mode | Overall Hit | Overall P | Overall R | Answer Weighted | Rated | Exact Hit | Prox Hit | Fuzzy Hit |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Latest (post rewrite hardening) | 20260602-180055-realistic_args | realistic_args | 0.500 | 0.142 | 0.283 | 0.577 | 26 | 0.500 | 0.200 | 0.800 |
| Latest (post rewrite hardening) | 20260602-180514-user | user | 0.433 | 0.120 | 0.250 | 0.550 | 30 | 0.500 | 0.000 | 0.800 |
| Latest (post rewrite hardening) | 20260602-181105-diagnostic_args | diagnostic_args | 0.667 | 0.280 | 0.489 | 0.650 | 30 | 0.700 | 0.400 | 0.900 |
| Session 2 | 20260602-173138-realistic_args | realistic_args | 0.333 | 0.095 | 0.183 | 0.433 | 30 | 0.000 | 0.200 | 0.800 |
| Session 2 | 20260602-173432-user | user | 0.267 | 0.073 | 0.150 | 0.333 | 30 | 0.000 | 0.000 | 0.800 |
| Session 2 | 20260602-173656-diagnostic_args | diagnostic_args | 0.567 | 0.267 | 0.411 | 0.467 | 30 | 0.400 | 0.400 | 0.900 |
| Session 1 | 20260602-160128-realistic_args | realistic_args | 0.300 | 0.082 | 0.161 | 0.400 | 30 | 0.000 | 0.100 | 0.800 |
| Session 1 | 20260602-161413-user | user | 0.267 | 0.073 | 0.150 | 0.333 | 30 | 0.000 | 0.000 | 0.800 |
| Session 1 | 20260602-161506-diagnostic_args | diagnostic_args | 0.567 | 0.282 | 0.428 | 0.467 | 30 | 0.400 | 0.400 | 0.900 |
| Building Gold Truth | 20260528-194915-diagnostic_args | diagnostic_args | n/a | n/a | n/a | 0.500 | 30 | n/a | n/a | n/a |
| Building Gold Truth | 20260602-155543-diagnostic_args | diagnostic_args | 0.000 | 0.000 | 0.000 | n/a | 0 | 0.000 | 0.000 | 0.000 |

## 6) Delta-Analyse (Session 1 -> Session 2 -> Latest)

### 6.1 Realistic Args
- Overall Hit: 0.300 -> 0.333 -> 0.500
- Overall Weighted Answer: 0.400 -> 0.433 -> 0.577
- Exact Hit: 0.000 -> 0.000 -> 0.500
- Prox Hit: 0.100 -> 0.200 -> 0.200
- Fuzzy Hit: 0.800 -> 0.800 -> 0.800

### 6.2 User
- Overall Hit: 0.267 -> 0.267 -> 0.433
- Overall Weighted Answer: 0.333 -> 0.333 -> 0.550
- Exact Hit: 0.000 -> 0.000 -> 0.500
- Prox Hit: 0.000 -> 0.000 -> 0.000
- Fuzzy Hit: 0.800 -> 0.800 -> 0.800

### 6.3 Diagnostic Args
- Overall Hit: 0.567 -> 0.567 -> 0.667
- Overall Weighted Answer: 0.467 -> 0.467 -> 0.650
- Exact Hit: 0.400 -> 0.400 -> 0.700
- Prox Hit: 0.400 -> 0.400 -> 0.400
- Fuzzy Hit: 0.900 -> 0.900 -> 0.900

## 7) Erkenntnisse (fachlich + technisch)

### 7.1 Was klar funktioniert
- Serverseitiger Rewrite fuer Exact ist der entscheidende Hebel fuer natuerliche Nutzerfragen.
- Fuzzy ist robust und aktuell die stabilste Retrieval-Strategie ueber alle Modi.
- Geteilte Chunk-Goldtruth verbessert Vergleichbarkeit und Wartbarkeit der Testbench deutlich.
- Multi-PDF-Ingestion mit korrekten Seitenmetadaten ist Grundlage fuer belastbare Review/Traceability.

### 7.2 Wo aktuell Grenzen liegen
- Proximity zeigt trotz Rewrite noch keine sichtbare Verbesserung in den aktuellen Metriken.
- Einzelne Altruns sind methodisch nicht direkt vergleichbar (Goldtruth-Aufbauphase, fehlende Ratings oder fehlende Retrieval-Eval).
- Ein Lauf hat nur 26 statt 30 Ratings (realistic latest), dadurch leichte Antwort-Metrik-Vorsicht bei Vergleichen.

### 7.3 Methodische Konsequenz
- Fuer harte Vorher/Nachher-Aussagen die drei Modus-Runs immer als Triplet vergleichen (gleiches Zeitfenster, gleiche Spezifikation, gleiche Rating-Abdeckung).

## 8) Aktueller Arbeitsstand je Zielbereich

- Retrieval-Qualitaet: verbessert (insb. Exact).
- Antwortqualitaet: in den neuesten Runs ebenfalls verbessert (Weighted Score deutlich hoeher).
- Skalierbarkeit: technische Grundlage fuer >100 PDFs geschaffen (rekursiv, reset/replace, Metadaten).
- Reproduzierbarkeit: Run-Artefakte und Scoring-Workflow sind stabil und wiederholbar.

## 9) Offene Punkte fuer den naechsten Schritt

- Proximity gezielt nachschaerfen (z.B. term extraction, slop-Strategie, ggf. alternative query clauses).
- Optional: Aggregations-Skript fuer automatische Langzeit-Reporting-Datei (z.B. `experiments/aggregate_runs.py`).
- Konsistente Vollbewertung aller aktuellen Runs (30/30), um Antwortmetriken exakt vergleichbar zu halten.

## 10) Relevante Artefakte (Auswahl)

- Aktuelle Run-Scores:
  - `experiments/runs/20260602-180055-realistic_args/score-summary-realistic_args.txt`
  - `experiments/runs/20260602-180514-user/score-summary-user.txt`
  - `experiments/runs/20260602-181105-diagnostic_args/score-summary-diagnostic_args.txt`
- Vergleichskohorten:
  - `experiments/runs/session 1/...`
  - `experiments/runs/Session 2 - improving exact and proximity/...`
- Kerncode:
  - `ingestion/ingest.py`
  - `mcp-server/index.ts`
  - `experiments/run_testbench.py`
  - `experiments/score_testbench.py`
