# Pandoc PDF Build

Dieses Setup erzeugt aus `docs/Report.md` ein PDF mit Header/Footer, eingebetteten Grafiken, Tabellen und optionalen Mermaid-Diagrammen.

Das Abstract auf der Titelseite wird automatisch aus `docs/Abstract.md` gelesen.

## Voraussetzungen

- pandoc
- tectonic (Standard PDF-Engine)
- optional: mermaid-cli (`mmdc`) fuer `.mmd` -> `.png`

Installation auf macOS:

```bash
brew install pandoc tectonic
npm install -g @mermaid-js/mermaid-cli
```

## Build ausfuehren

Vom Projekt-Root:

```bash
./docs/pandoc/build-report.sh
```

Standard:

- Input: `docs/Report.md`
- Output: `docs/Report.pdf`
- Abstract: `docs/Abstract.md`

Eigenes Input/Output:

```bash
./docs/pandoc/build-report.sh docs/Report.md docs/Report-v2.pdf
```

Mit expliziter Abstract- und Bibliographie-Datei:

```bash
./docs/pandoc/build-report.sh docs/Report.md docs/Report-v2.pdf docs/Abstract.md docs/references.bib
```

Eigenes Abstract (optional drittes Argument):

```bash
./docs/pandoc/build-report.sh docs/Report.md docs/Report-v2.pdf docs/Abstract.md
```

Andere PDF-Engine:

```bash
PDF_ENGINE=xelatex ./docs/pandoc/build-report.sh
```

## Einbettung im Markdown

Bild:

```md
![Systemarchitektur](assets/architektur.png)
```

Mermaid:

1. Datei anlegen: `docs/assets/mermaid/diagramm.mmd`
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

- `docs/references.bib`

Zitieren im Text (Pandoc-Syntax):

```md
RAG wurde in der Literatur frueh etabliert [@lewis2020rag].

MCP ist ein zentraler Interoperabilitaetsansatz [vgl. @mcpdocs].

Siehe Elastic-Dokumentation fuer Mapping-Details [@elasticsearch].
```

Beim Build wird das Quellenverzeichnis automatisch als Abschnitt `Literaturverzeichnis` am Ende erzeugt.
Optional kann ein CSL-Stil unter `docs/pandoc/citation-style.csl` abgelegt werden.

## Troubleshooting

- Bilder fehlen: Pfade relativ zu `docs/Report.md` verwenden.
- Header/Footer fehlt: Datei `docs/pandoc/header-footer.tex` pruefen.
- Mermaid wird nicht gerendert: `mmdc` installieren.
