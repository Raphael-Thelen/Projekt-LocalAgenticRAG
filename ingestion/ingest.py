import argparse
import os
import re
from pathlib import Path

import pymupdf4llm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from langchain_text_splitters import RecursiveCharacterTextSplitter


INDEX_NAME = "lara_documents"
ES_HOST = "http://127.0.0.1:9200"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_DIR = SCRIPT_DIR.parent / "data"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Indexiert rekursiv PDFs in Elasticsearch (Batch-fähig)."
    )
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--index", type=str, default=INDEX_NAME)
    parser.add_argument("--es-host", type=str, default=ES_HOST)
    parser.add_argument("--glob", type=str, default="**/*.pdf")
    parser.add_argument("--chunk-size", type=int, default=1100)
    parser.add_argument("--chunk-overlap", type=int, default=180)
    parser.add_argument(
        "--reset-index",
        action="store_true",
        help="Loescht den gesamten Index und erstellt ihn neu.",
    )
    parser.add_argument(
        "--replace-doc",
        action="store_true",
        help="Loescht vor dem Re-Indexing nur Chunks desselben Dokuments (doc_id).",
    )
    return parser


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value)
    return value.strip("_") or "document"


def build_doc_id(pdf_path: Path, data_dir: Path) -> str:
    rel = pdf_path.relative_to(data_dir)
    stem = rel.with_suffix("")
    parts = [slugify(part) for part in stem.parts]
    return "__".join(parts)


def setup_elasticsearch(es_host: str, index_name: str, reset_index: bool) -> Elasticsearch:
    """Verbindet sich mit ES und stellt den Index inkl. Mapping sicher."""
    os.environ["no_proxy"] = "*"

    es = Elasticsearch(es_host)
    try:
        info = es.info()
        print(f"--- Erfolgreich verbunden! Elasticsearch Version: {info['version']['number']} ---")
    except Exception as exc:
        print(f"Fehler bei der Verbindung zu Elasticsearch:\n{exc}")
        raise ConnectionError("Abbruch wegen Verbindungsfehler.") from exc

    mapping = {
        "mappings": {
            "properties": {
                "doc_id": {"type": "keyword"},
                "chunk_id": {"type": "keyword"},
                "title": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"},
                    },
                },
                "source": {"type": "keyword"},
                "page": {"type": "integer"},
                "file_path": {"type": "keyword"},
                "content": {
                    "type": "text",
                    "analyzer": "german",
                },
            }
        }
    }

    exists = es.indices.exists(index=index_name)
    if reset_index and exists:
        es.indices.delete(index=index_name)
        print(f"Alten Index '{index_name}' geloescht.")
        exists = False

    if not exists:
        es.indices.create(index=index_name, body=mapping)
        print(f"Index '{index_name}' bereit.")
    else:
        print(f"Index '{index_name}' existiert bereits (inkrementeller Modus).")

    return es


def list_pdf_files(data_dir: Path, pattern: str) -> list[Path]:
    return sorted(path for path in data_dir.glob(pattern) if path.is_file())


def get_page_number(page_data: dict) -> int:
    metadata = page_data.get("metadata", {}) if isinstance(page_data, dict) else {}

    page_number = metadata.get("page_number")
    if isinstance(page_number, int):
        return page_number

    legacy_page = metadata.get("page")
    if isinstance(legacy_page, int):
        return legacy_page + 1

    return 1


def extract_and_chunk_pdf(
    pdf_path: Path,
    data_dir: Path,
    index_name: str,
    text_splitter: RecursiveCharacterTextSplitter,
) -> tuple[str, list[dict]]:
    print(f"Lese PDF: {pdf_path}")

    md_pages = pymupdf4llm.to_markdown(str(pdf_path), page_chunks=True)
    doc_id = build_doc_id(pdf_path, data_dir)
    title = pdf_path.stem
    file_path = str(pdf_path.relative_to(data_dir))

    documents: list[dict] = []
    for page_data in md_pages:
        page_num = get_page_number(page_data)
        text = str(page_data.get("text", "")) if isinstance(page_data, dict) else ""
        chunks = text_splitter.split_text(text)

        for chunk_index, chunk in enumerate(chunks):
            clean_chunk = chunk.strip()
            if not clean_chunk:
                continue

            chunk_id = f"{doc_id}_p{page_num}_c{chunk_index:03d}"
            documents.append(
                {
                    "_index": index_name,
                    "_source": {
                        "doc_id": doc_id,
                        "chunk_id": chunk_id,
                        "title": title,
                        "source": doc_id,
                        "page": page_num,
                        "file_path": file_path,
                        "content": clean_chunk,
                    },
                }
            )

    print(f"  -> {doc_id}: {len(documents)} Chunks")
    return doc_id, documents


def replace_doc_chunks(es: Elasticsearch, index_name: str, doc_id: str) -> int:
    response = es.delete_by_query(
        index=index_name,
        body={"query": {"term": {"doc_id": doc_id}}},
        conflicts="proceed",
        refresh=True,
        wait_for_completion=True,
    )
    return int(response.get("deleted", 0))


def main() -> None:
    args = build_parser().parse_args()
    data_dir = args.data_dir.resolve()

    if not data_dir.exists():
        raise FileNotFoundError(f"Data-Ordner nicht gefunden: {data_dir}")

    if args.chunk_overlap >= args.chunk_size:
        raise ValueError("chunk_overlap muss kleiner als chunk_size sein.")

    es = setup_elasticsearch(
        es_host=args.es_host,
        index_name=args.index,
        reset_index=args.reset_index,
    )

    pdf_files = list_pdf_files(data_dir, args.glob)
    if not pdf_files:
        print(f"Keine PDFs gefunden in {data_dir} mit Muster '{args.glob}'.")
        return

    print(f"Gefundene PDFs: {len(pdf_files)}")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )

    total_success = 0
    total_failed = 0
    total_deleted = 0

    for pdf_path in pdf_files:
        try:
            doc_id, docs = extract_and_chunk_pdf(
                pdf_path=pdf_path,
                data_dir=data_dir,
                index_name=args.index,
                text_splitter=text_splitter,
            )

            if args.replace_doc:
                deleted = replace_doc_chunks(es, args.index, doc_id)
                total_deleted += deleted
                print(f"  -> Vorhandene Chunks fuer {doc_id} geloescht: {deleted}")

            if not docs:
                print(f"  -> Uebersprungen (keine Chunks): {pdf_path}")
                continue

            success, failed = bulk(es, docs, raise_on_error=False)
            total_success += int(success)
            total_failed += len(failed)
            print(f"  -> Indexiert: {success}, Fehler: {len(failed)}")
        except Exception as exc:
            total_failed += 1
            print(f"Fehler bei {pdf_path}: {exc}")

    print("\n===== Ingestion abgeschlossen =====")
    print(f"PDFs verarbeitet: {len(pdf_files)}")
    print(f"Geloeschte Alt-Chunks (replace-doc): {total_deleted}")
    print(f"Erfolgreich indexierte Chunks: {total_success}")
    print(f"Fehlgeschlagene Bulk-Operationen: {total_failed}")


if __name__ == "__main__":
    main()