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
GEMINI_MODEL_NAME=gemini-2.5-flash
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
python experiments/model_compare/run_model_compare.py
```
