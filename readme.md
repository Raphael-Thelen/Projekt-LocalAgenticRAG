<!--
Hier ist deine komplette README.md als ungerenderter Quellcode,
genau wie von dir gewünscht. Du kannst alles ab dem h1-Tag (#)
direkt in deine Datei kopieren.
-->

# Projekt L.A.R.A.

**L**ocal **A**gentic **R**etrieval **A**rchitecture

L.A.R.A. ist ein Forschungsprototyp (Stand: Mai 2026) zur Evaluation von privatsphärendem, lokalem "Agentic RAG" (Retrieval-Augmented Generation). Das System kombiniert komplexe lokale PDF-Dokumente, Elasticsearch, das Model Context Protocol (MCP) und lokale Large Language Models (LLMs) zu einer vollständig offline-fähigen Chat-Architektur.

## Systemvoraussetzungen

- **Hardware:** Apple Silicon (M1/M2/M3) mit min. 8 GB RAM (16 GB empfohlen).
- **Docker & Docker Compose:** Für den Elasticsearch-Container.
- **Node.js (v20+):** Für den TypeScript MCP-Server.
- **Python (3.10+):** Für die Ingestion-Pipeline und den KI-Agenten.
- **Ollama:** Lokal installiert (als macOS Cask-App für M-Chip Beschleunigung).

---

## Projektstruktur

```text
lara-project/
├── data/          # Enthält die Rohdaten (lokale PDFs)
├── docker/        # Docker-Compose Konfiguration (Elasticsearch & Kibana)
├── ingestion/     # Python-Skript (PyMuPDF4LLM) zum Parsen & Indexieren
├── mcp-server/    # TypeScript MCP-Server (Stellt Such-Tools für die KI bereit)
└── mcp-client/    # Python MCP-Client (Der Mistral Agentic Loop)
```

---

## Schritt-für-Schritt Startanleitung

### 1. Lokales KI-Modell hochfahren

Stelle sicher, dass die Ollama-App auf dem Mac im Hintergrund läuft (Sichtbar im System-Tray). Lade und starte das Mistral-Modell:

```bash
ollama run mistral
```

_(Du kannst das Terminal danach schließen, der Dienst läuft im Hintergrund auf `http://localhost:11434` weiter)._

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

## Fehlerbehebung (Troubleshooting für Apple M1)

- **Mac wird extrem langsam (Swapping):** Elasticsearch, Docker und das 7B-Modell von Mistral benötigen zusammen ca. 6-7 GB Unified Memory. Schließe bei einem 8GB Mac RAM-hungrige Anwendungen (wie dutzende Browser-Tabs) während der Ausführung von `agent.py`.
- **Elasticsearch Connect Error:** Stelle sicher, dass in Docker keine alten Container auf Port `9200` laufen und die `docker-compose.yml` korrekt mit `xpack.security.enabled=false` konfiguriert ist.

## Modell-Vergleich (Plug & Play)

Um für Evaluationen verschiedene Modelle zu testen:

1. Lade ein neues Modell via Ollama (z.B. `ollama pull qwen2.5:7b-instruct`).
2. Öffne `mcp-client/agent.py`.
3. Ändere die Konstante `MODEL_NAME = "mistral"` zum neuen Modellnamen.
4. Führe `agent.py` erneut aus.
