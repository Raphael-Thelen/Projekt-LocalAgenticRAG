# Pandoc PDF Build

Dieses Setup erzeugt aus `docs/Bericht/Report.md` ein PDF mit Header/Footer, eingebetteten Grafiken, Tabellen und optionalen Mermaid-Diagrammen.

Das Abstract auf der Titelseite wird automatisch aus `docs/Bericht/Abstract.md` gelesen.

## Voraussetzungen

- pandoc
- tectonic (Standard PDF-Engine)
- optional: mermaid-cli (`mmdc`) fuer `.mmd` -> `.png`

Installation auf macOS:

```bash
brew install pandoc tectonic
npm install -g @mermaid-js/mermaid-cli
```

## Build ausführen

Im Berichtsverzeichnis kann der Standard-Build über das dortige `package.json` gestartet werden:

```bash
cd docs/Bericht
npm run build
```

Alternativ direkt vom Projekt-Root:

```bash
./docs/Bericht/pandoc/build-report.sh
```

Standard:

- Input: `docs/Bericht/Report.md`
- Output: `docs/Bericht/Report.pdf`
- Abstract: `docs/Bericht/Abstract.md`
- Bibliographie: `docs/Bericht/references.bib`
- PDF-Engine: `tectonic`

Eigenes Input/Output:

```bash
./docs/Bericht/pandoc/build-report.sh \
  docs/Bericht/Report.md \
  docs/Bericht/Report-v2.pdf
```

Mit expliziter Abstract- und Bibliographie-Datei:

```bash
./docs/Bericht/pandoc/build-report.sh \
  docs/Bericht/Report.md \
  docs/Bericht/Report-v2.pdf \
  docs/Bericht/Abstract.md \
  docs/Bericht/references.bib
```

Eigenes Abstract (optional drittes Argument):

```bash
./docs/Bericht/pandoc/build-report.sh \
  docs/Bericht/Report.md \
  docs/Bericht/Report-v2.pdf \
  docs/Bericht/Abstract.md
```

Andere PDF-Engine:

```bash
PDF_ENGINE=xelatex ./docs/Bericht/pandoc/build-report.sh
```

## Einbettung im Markdown

Bild:

```md
![Systemarchitektur](assets/architektur.png)
```

Mermaid:

1. Datei anlegen: `docs/Bericht/assets/mermaid/diagramm.mmd`
2. Build starten (Script rendert automatisch nach `diagramm.png`)
3. PNG in Markdown einbinden:

```md
![Komponentendiagramm](assets/mermaid/diagramm.png)
```

Tabelle (Markdown):

```md
| Tool | Precision@5 | Recall@5 |
|---|---:|---:|
| search_fuzzy | 0.92 | 1.00 |
| search_exact_keyword | 0.90 | 1.00 |
```

## Zitate und Quellenverzeichnis

BibTeX-Datei:

- `docs/Bericht/references.bib`

Zitieren im Text (Pandoc-Syntax):

```md
RAG wurde in der Literatur frueh etabliert [@lewis2020rag].

MCP ist ein zentraler Interoperabilitaetsansatz [vgl. @mcpdocs].

Siehe Elastic-Dokumentation fuer Mapping-Details [@elasticsearch].
```

Beim Build wird das Quellenverzeichnis automatisch als Abschnitt `Literaturverzeichnis` am Ende erzeugt.
Optional kann ein CSL-Stil unter `docs/Bericht/pandoc/citation-style.csl` abgelegt werden.

## Troubleshooting

- Bilder fehlen: Pfade relativ zu `docs/Bericht/Report.md` verwenden.
- Header/Footer fehlt: Datei `docs/Bericht/pandoc/header-footer.tex` prüfen.
- Mermaid wird nicht gerendert: `mmdc` installieren.
