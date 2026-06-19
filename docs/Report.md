## Arbeitstitel

Lokales Agentic-RAG mit MCP und Elasticsearch fuer PDF-Wissensbestaende: Konzeption, Implementierung und Evaluation am Beispiel eines DSA-Regelwerkskorpus

## Inhaltsverzeichnis

### 1. Einleitung (ca. 2 Seiten)

1.1 Problemstellung und Motivation

1.2 Zielsetzung der Arbeit

1.3 Forschungsfrage und Teilfragen

1.4 Abgrenzung des Projekts

1.5 Aufbau der Arbeit

### 2. Technische und fachliche Grundlagen (ca. 3 Seiten) -> evtl. Zuschicken

2.1 Retrieval-Augmented Generation und Agentic-RAG

2.2 Model Context Protocol als Werkzeugschicht fuer LLM-Systeme

2.3 Elasticsearch als lokale Retrieval-Komponente

2.4 PDF-Ingestion, Chunking und Metadaten

2.5 Evaluationsmetriken fuer Retrieval und Antwortqualitaet

### 3. Anforderungsanalyse und Zielarchitektur (ca. 1 Seiten, mit UML Diagramm, Komponenten Diagramm, Squence Diagramm)

3.1 Anforderungen an ein lokales und privatsphaerisches Assistenzsystem

3.2 Funktionale Anforderungen

3.3 Nicht-funktionale Anforderungen

3.4 Zielarchitektur des Systems

### 4. Systementwurf und Implementierung (ca. 1 Seiten, Klassendiagramm, Sourcecode snippets, Dokumentation im SC)

4.1 Gesamtpipeline vom PDF-Dokument bis zur Antwort

4.2 Dateningestion und Indexaufbau

4.3 Elasticsearch-Mapping und Dokumentstruktur

4.4 MCP-Server und Such-Tools

4.5 LLM-Client, Tool-Nutzung und Antwortgenerierung

4.6 Reproduzierbarkeit, Logging und Artefaktstruktur

### 5. Entwicklung der Retrieval-Strategien (ca. 3 Seiten)

5.1 Ausgangspunkt: einfacher Einzel-PDF-Prototyp

5.2 Exact Retrieval und Query-Rewrite

5.3 Phrase- und Proximity-Retrieval

5.4 Fuzzy Retrieval als robuster Baseline-Ansatz (prüfen)

5.5 KI-gestuetztes Smart Retrieval: Idee, Umsetzung und Grenzen

### 6. Evaluationsdesign (ca. 3 Seiten)

6.1 Aufbau der Testbench

6.2 Fragenset, Modi und Goldtruth-Konzept

6.3 Bewertungslogik fuer Retrieval

6.4 Manuelle Bewertung der Antwortqualitaet

6.5 Versuchsaufbau und Vergleichbarkeit der Runs

### 7. Experimentelle Ergebnisse (ca. 3 Seiten)

7.1 Ergebnisse der fruehen Runs und Iterationen

7.2 Verbesserungen durch Exact-Rewrite

7.3 Vergleich von Exact, Proximity und Fuzzy

7.4 Vergleich Fuzzy vs. Smart im User-Mode

7.5 Vergleich Gemini API vs. Lokale Modelle

7.6 Zusammenfassung der zentralen quantitativen Befunde

### 8. Diskussion (ca. 3 Seiten)

8.1 Einordnung der Retrieval-Ergebnisse

8.2 Warum Fuzzy aktuell der staerkste Ansatz ist

8.3 Grenzen von Exact und Proximity

8.4 Grenzen des aktuellen Smart-Retrieval-Ansatzes

8.5 Validitaet der Metriken und Grenzen der Goldtruth

### 9. Fazit und Ausblick (ca. 1 Seiten)

9.1 Beantwortung der Forschungsfrage

9.2 Wichtigste technische und methodische Erkenntnisse

9.3 Konkrete naechste Entwicklungsschritte

9.4 Perspektiven fuer weiterfuehrende Forschung

## Optionaler Anhang

### A. Relevante Kommandozeilenbefehle

### B. Beispielhafte Run-Artefakte

### C. Beispielhafte Benchmark-Fragen

### D. Tabellen mit Detailmetriken

## Empfehlung fuer den roten Faden

Die Arbeit sollte argumentativ auf folgende Kernaussage zulaufen:

Ein lokales Agentic-RAG-System mit MCP und Elasticsearch ist fuer PDF-Wissensbestaende praktikabel umsetzbar, reproduzierbar evaluierbar und liefert bereits in einer einfachen Retrieval-Konfiguration nuetzliche Ergebnisse. Unter den untersuchten Retrieval-Strategien erweist sich Fuzzy Retrieval im aktuellen Systemstand als robustester und insgesamt geeignetster Ansatz fuer natuerliche Nutzeranfragen, waehrend Exact und Proximity eher spezialisierte oder nachrangige Rollen einnehmen.