# Projekt L.A.R.A.

**L**ocal **A**gentic **R**etrieval **A**rchitecture

L.A.R.A. ist ein Forschungsprototyp (Stand: Mai 2026) zur Evaluation von privatsphärendem, lokalem "Agentic RAG" (Retrieval-Augmented Generation). Das System kombiniert komplexe lokale PDF-Dokumente, Elasticsearch, das Model Context Protocol (MCP) und lokale Large Language Models (LLMs) zu einer vollständig offline-fähigen Chat-Architektur.

Aktuell ist ein Hybrid-Betrieb vorgesehen: Gemini API fuer schnelle Entwicklung auf schwacher Hardware, spaeter lokale Modelle auf einem staerkeren PC.

Dokumentationsprozess: Alle Umsetzungsstaende, Testlaeufe und Zwischenergebnisse werden fortlaufend in docs/diary.md gepflegt.

## Systemvoraussetzungen

- **Hardware:** Apple Silicon (M1/M2/M3) mit min. 8 GB RAM (16 GB empfohlen).
- **Docker & Docker Compose:** Für den Elasticsearch-Container.
- **Node.js (v20+):** Für den TypeScript MCP-Server.
- **Python (3.10+):** Für die Ingestion-Pipeline und den KI-Agenten.
- **Gemini API Key:** Fuer den Cloud-basierten Entwicklungsmodus.
- **Ollama (optional):** Fuer spaetere lokale Modelltests.

---

## Projektstruktur

```text
lara-project/
├── data/          # Enthält die Rohdaten (lokale PDFs)
├── docker/        # Docker-Compose Konfiguration (Elasticsearch & Kibana)
├── ingestion/     # Python-Skript (PyMuPDF4LLM) zum Parsen & Indexieren
├── mcp-server/    # TypeScript MCP-Server (Stellt Such-Tools für die KI bereit)
├── mcp-client/    # Python MCP-Client (Agentic Loop mit Gemini/Ollama)
└── .env.example   # Beispielkonfiguration fuer LLM-Provider
```

---

## Schritt-für-Schritt Startanleitung

### 1. LLM-Provider konfigurieren (Gemini empfohlen)

Im Projekt-Root eine lokale .env anlegen und Provider setzen:

```bash
cp .env.example .env
```

Dann in .env mindestens den API Key eintragen:

```env
LARA_LLM_PROVIDER=gemini
GEMINI_API_KEY=dein_key
GEMINI_MODEL_NAME=gemini-3.1-flash-lite
```

Optional fuer lokale Tests spaeter:

```env
LARA_LLM_PROVIDER=ollama
OLLAMA_MODEL_NAME=llama3.1
```

### 2. Infrastruktur (Elasticsearch) starten

Navigiere im Terminal in den Docker-Ordner und starte die Datenbank.

```bash
cd docker
docker compose up -d
```

Warte ca. 1-2 Minuten. Du kannst unter [http://localhost:5601](http://localhost:5601) prüfen, ob Kibana erreichbar ist.

### 3. Daten aufbereiten und indizieren (Ingestion)

Lege zunächst dein PDF (z.B. `dsa_regelwerk.pdf`) in den Ordner `data/`.
Richte dann die Python-Umgebung ein und starte den Indexierungs-Vorgang:

```bash
cd ../ingestion
python3 -m venv venv
source venv/bin/activate
pip install pymupdf4llm langchain-text-splitters
pip install "elasticsearch==8.13.0"
python ingest.py
```

_(Das Skript zerschneidet das PDF in Chunks und sendet sie an Elasticsearch)._

### 4. MCP-Server Abhängigkeiten installieren

Der Server kommuniziert später über das `stdio`-Protokoll mit dem Python-Agenten. Wir müssen nur einmalig die Node-Pakete installieren:

```bash
cd ../mcp-server
npm install
```

### 5. Den L.A.R.A. Agenten starten (Der Test)

Schließlich betreten wir das Client-Verzeichnis, richten eine zweite Python-Umgebung ein (um Abhängigkeiten sauber zu trennen) und starten den Agentic Loop.

```bash
cd ../mcp-client
python3 -m venv venv
source venv/bin/activate
pip install mcp openai

# Starte den KI-Agenten
python agent.py
```

Der Agent liest automatisch die .env aus dem Projekt-Root und zeigt beim Start den aktiven Provider an.

### Optional: Lokales Modell mit Ollama starten

Nur falls in .env `LARA_LLM_PROVIDER=ollama` gesetzt ist:

```bash
ollama run llama3.1
```

## Fehlerbehebung (Troubleshooting für Apple M1)

- **Mac wird extrem langsam (Swapping):** Elasticsearch, Docker und das 7B-Modell von Mistral benötigen zusammen ca. 6-7 GB Unified Memory. Schließe bei einem 8GB Mac RAM-hungrige Anwendungen (wie dutzende Browser-Tabs) während der Ausführung von `agent.py`.
- **Elasticsearch Connect Error:** Stelle sicher, dass in Docker keine alten Container auf Port `9200` laufen und die `docker-compose.yml` korrekt mit `xpack.security.enabled=false` konfiguriert ist.

## Modell-Vergleich (Plug & Play)

Um für Evaluationen verschiedene Modelle zu testen:

1. Fuer Cloud-Tests: In .env `GEMINI_MODEL_NAME` wechseln.
2. Fuer lokale Tests: In .env `LARA_LLM_PROVIDER=ollama` setzen und `OLLAMA_MODEL_NAME` anpassen.
3. Agent erneut starten und Latenz/Qualitaet vergleichen.

## Evaluation und Berichtsartefakte

Aktuelle Kernartefakte fuer Retrieval-Evaluation und Modellvergleich:

- Retrieval-Runner: `experiments/eval/run_eval.py`
- Gold-Truth (aktuell): `experiments/eval/gold-truth-v4.csv`
- Eval-Report (aktuell): `experiments/eval/eval-report-v4.md`
- Testbench-Spezifikation (10 Fragen): `experiments/eval/testbench-v1.json`
- Testbench-Runner: `experiments/eval/run_testbench.py`
- Testbench-Scorer: `experiments/eval/score_testbench.py`
- Modellvergleich-Runner: `experiments/model_compare/run_model_compare.py`
- Modellvergleich-Konfiguration: `experiments/model_compare/query-set.json`
- Modellvergleich-Report: `experiments/model_compare/model-compare-report.md`

Beispiel: Eval laufen lassen

```bash
source .venv/bin/activate
python experiments/eval/run_eval.py \
	--input experiments/eval/gold-truth-v4.csv \
	--output experiments/eval/eval-report-v4.md \
	--title '# Eval Report v4'
```

Beispiel: Modellvergleich laufen lassen

```bash
source .venv/bin/activate
python3 experiments/model_compare/run_model_compare.py
```

### Neuer Testbench-Workflow (Chunk + Antwortbewertung)

Der Testbench trennt Retrieval und Antwortbewertung bewusst:

1. Der Runner erzeugt pro Lauf einen Run-Ordner mit Rohdaten und einer manuellen Bewertungsdatei.
2. Du bewertest die KI-Antworten in `manual-review-<mode>.txt` mit `C/P/W`.
3. Nach dem Schliessen der Datei berechnet der Scorer die Kennzahlen.

Verfuegbare Modi:

- `user`: nutzt direkt das Feld `question` aus der JSON als Tool-Eingabe.
- `realistic_args`: nutzt `realistic_tool_args` aus der JSON.
- `diagnostic_args`: nutzt `diagnostic_tool_args` aus der JSON (technische Diagnose, nicht Hauptbenchmark).

Wichtige CLI-Argumente:

- `--provider gemini|ollama`
- `--model <modellname>` (optional)
- `--tools all|search_exact_keyword,search_fuzzy,search_phrase_proximity`
- `--mode user|realistic_args|diagnostic_args`
- `--max-retries`, `--retry-base-seconds`, `--retry-max-seconds`, `--retry-jitter-seconds` fuer adaptives Warten bei Quota/Rate-Limit
- `--score-after-review` (Editor wird mit `--wait` geoeffnet, danach Scoring)

Beispiel: realistischer Lauf ueber alle drei Tools

```bash
source .venv/bin/activate
python3 experiments/eval/run_testbench.py \
	--provider gemini \
	--mode realistic_args \
	--tools all \
	--max-retries 20 \
	--retry-base-seconds 30 \
	--retry-max-seconds 600 \
	--retry-jitter-seconds 3 \
	--score-after-review
```

Beispiel: User-Modus (echte Nutzerfrage direkt als Query)

```bash
source .venv/bin/activate
python3 experiments/eval/run_testbench.py \
	--provider gemini \
	--mode user \
	--tools all \
	--max-retries 20 \
	--retry-base-seconds 30 \
	--retry-max-seconds 600 \
	--retry-jitter-seconds 3 \
	--score-after-review
```

Beispiel: Nur Scoring fuer einen vorhandenen Lauf

```bash
python3 experiments/eval/score_testbench.py \
	--run-json experiments/eval/runs/<RUN_ID>/run-<MODE>.json \
	--review-txt experiments/eval/runs/<RUN_ID>/manual-review-<MODE>.txt
```

Erzeugte Dateien pro Lauf (im jeweiligen `experiments/eval/runs/<RUN_ID>-<MODE>/`):

- `run-<mode>.json`: Vollstaendige maschinenlesbare Rohdaten (Retrieval + Antworten + Metadaten).
- `manual-review-<mode>.txt`: Manuelle C/P/W-Bewertung pro Frage und Tool.
- `score-<mode>.json`: Kennzahlen als JSON.
- `score-summary-<mode>.txt`: Menschlich lesbare Zusammenfassung.
- `spec.snapshot.json`: Eingefrorene Spezifikation des Laufs fuer Reproduzierbarkeit.
