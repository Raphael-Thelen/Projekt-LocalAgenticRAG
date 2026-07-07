#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DOCS_DIR="$ROOT_DIR/docs"
PANDOC_DIR="$DOCS_DIR/pandoc"

INPUT_MD="${1:-$DOCS_DIR/Report.md}"
OUTPUT_PDF="${2:-$DOCS_DIR/Report.pdf}"
ABSTRACT_MD="${3:-$DOCS_DIR/Abstract.md}"
BIB_FILE="${4:-$DOCS_DIR/references.bib}"
CSL_FILE="${5:-$PANDOC_DIR/citation-style.csl}"
HEADER_FILE="$PANDOC_DIR/header-footer.tex"
TITLEPAGE_FILE="$PANDOC_DIR/titlepage.tex"
MERMAID_DIR="$DOCS_DIR/assets/mermaid"
PDF_ENGINE="${PDF_ENGINE:-tectonic}"

if ! command -v pandoc >/dev/null 2>&1; then
  echo "Error: pandoc not found. Install with: brew install pandoc"
  exit 1
fi

if ! command -v "$PDF_ENGINE" >/dev/null 2>&1; then
  echo "Error: PDF engine '$PDF_ENGINE' not found."
  echo "Install tectonic with: brew install tectonic"
  echo "Or run with another engine, e.g.: PDF_ENGINE=xelatex $0"
  exit 1
fi

if [[ ! -f "$INPUT_MD" ]]; then
  echo "Error: input file not found: $INPUT_MD"
  exit 1
fi

if [[ ! -f "$HEADER_FILE" ]]; then
  echo "Error: header/footer file not found: $HEADER_FILE"
  exit 1
fi

if [[ ! -f "$TITLEPAGE_FILE" ]]; then
  echo "Error: titlepage file not found: $TITLEPAGE_FILE"
  exit 1
fi

if [[ ! -f "$ABSTRACT_MD" ]]; then
  echo "Error: abstract file not found: $ABSTRACT_MD"
  exit 1
fi

if [[ ! -f "$BIB_FILE" ]]; then
  echo "Error: bibliography file not found: $BIB_FILE"
  exit 1
fi

# Optional: render Mermaid source files to SVG before PDF generation.
if [[ -d "$MERMAID_DIR" ]]; then
  shopt -s nullglob
  mermaid_files=("$MERMAID_DIR"/*.mmd)
  if (( ${#mermaid_files[@]} > 0 )); then
    if command -v mmdc >/dev/null 2>&1; then
      echo "Rendering Mermaid diagrams..."
      for mmd in "${mermaid_files[@]}"; do
        svg="${mmd%.mmd}.svg"
        mmdc -q -i "$mmd" -o "$svg"
        echo "  -> $(basename "$svg")"
      done
    else
      echo "Warning: Mermaid files found, but mmdc is not installed."
      echo "Install with: npm install -g @mermaid-js/mermaid-cli"
      echo "Continuing without Mermaid rendering..."
    fi
  fi
fi

mkdir -p "$(dirname "$OUTPUT_PDF")"

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

abstract_tex="$tmp_dir/abstract.generated.tex"
titlepage_generated="$tmp_dir/titlepage.generated.tex"

echo "Rendering abstract from $ABSTRACT_MD ..."
pandoc "$ABSTRACT_MD" \
  --from markdown \
  --to latex \
  --output "$abstract_tex"

awk -v abstract_file="$abstract_tex" '
  $0 == "%%ABSTRACT%%" {
    while ((getline line < abstract_file) > 0) {
      print line
    }
    close(abstract_file)
    next
  }
  { print }
' "$TITLEPAGE_FILE" > "$titlepage_generated"

echo "Building PDF..."
PANDOC_CITATION_ARGS=(
  --citeproc
  --bibliography="$BIB_FILE"
  --metadata=reference-section-title:Literaturverzeichnis
  --metadata=link-citations:true
)

if [[ -f "$CSL_FILE" ]]; then
  PANDOC_CITATION_ARGS+=(--csl="$CSL_FILE")
else
  echo "Info: No CSL file found at $CSL_FILE, using Pandoc default citation style."
fi

pandoc "$INPUT_MD" \
  --standalone \
  --from markdown+pipe_tables+grid_tables+multiline_tables \
  --pdf-engine="$PDF_ENGINE" \
  --resource-path="$DOCS_DIR:$ROOT_DIR" \
  --number-sections \
  -V documentclass=report \
  -V lang=de-DE \
  -V geometry:a4paper \
  -V geometry:margin=2.5cm \
  -H "$HEADER_FILE" \
  --include-before-body="$titlepage_generated" \
  "${PANDOC_CITATION_ARGS[@]}" \
  -o "$OUTPUT_PDF"

echo "Done: $OUTPUT_PDF"
