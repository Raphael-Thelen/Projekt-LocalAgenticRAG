import argparse
import json
import os
import re
import urllib.error
import urllib.request
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
    parser.add_argument(
        "--enable-vectors",
        action="store_true",
        help="Berechnet Embeddings und speichert sie im Feld 'content_vector'.",
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default="nomic-embed-text",
        help="Ollama Embedding-Modell (Default: nomic-embed-text).",
    )
    parser.add_argument(
        "--embedding-api-url",
        type=str,
        default="http://127.0.0.1:11434/api/embeddings",
        help="Ollama Embedding API Endpoint.",
    )
    parser.add_argument(
        "--embedding-dims",
        type=int,
        default=0,
        help="Dimensionen fuer dense_vector (0 = automatisch ueber Probe bestimmen).",
    )
    parser.add_argument(
        "--embedding-timeout",
        type=float,
        default=30.0,
        help="Timeout in Sekunden fuer Embedding-Anfragen.",
    )
    parser.add_argument(
        "--embedding-fail-fast",
        action="store_true",
        help="Bricht bei Embedding-Fehlern sofort ab, statt ohne Vektor weiterzulaufen.",
    )
    return parser


class OllamaEmbedder:
    def __init__(self, api_url: str, model: str, timeout_seconds: float, expected_dims: int = 0):
        self.api_url = api_url
        self.model = model
        self.timeout_seconds = max(1.0, float(timeout_seconds))
        self.expected_dims = int(expected_dims)

    def _post(self, text: str) -> list[float]:
        payload = json.dumps({"model": self.model, "prompt": text}).encode("utf-8")
        request = urllib.request.Request(
            self.api_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
        parsed = json.loads(raw)
        embedding_raw = parsed.get("embedding", [])

        if not isinstance(embedding_raw, list) or not embedding_raw:
            raise ValueError("Embedding-Antwort enthaelt kein gueltiges 'embedding' Array.")

        vector = [float(value) for value in embedding_raw]
        if self.expected_dims > 0 and len(vector) != self.expected_dims:
            raise ValueError(
                f"Embedding-Dimension passt nicht zum Mapping (erwartet {self.expected_dims}, erhalten {len(vector)})."
            )
        return vector

    def probe_dimensions(self) -> int:
        vector = self._post("dimension-probe")
        return len(vector)

    def encode(self, text: str) -> list[float]:
        return self._post(text)


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


def setup_elasticsearch(
    es_host: str,
    index_name: str,
    reset_index: bool,
    enable_vectors: bool,
    embedding_dims: int,
) -> Elasticsearch:
    """Verbindet sich mit ES und stellt den Index inkl. Mapping sicher."""
    os.environ["no_proxy"] = "*"

    es = Elasticsearch(es_host)
    try:
        info = es.info()
        print(f"--- Erfolgreich verbunden! Elasticsearch Version: {info['version']['number']} ---")
    except Exception as exc:
        print(f"Fehler bei der Verbindung zu Elasticsearch:\n{exc}")
        raise ConnectionError("Abbruch wegen Verbindungsfehler.") from exc

    properties: dict = {
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

    if enable_vectors:
        properties["content_vector"] = {
            "type": "dense_vector",
            "dims": embedding_dims,
            "index": True,
            "similarity": "cosine",
        }

    mapping = {
        "mappings": {
            "properties": properties,
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
    embedder: OllamaEmbedder | None,
    embed_fail_fast: bool,
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

            if embedder is not None:
                try:
                    vector = embedder.encode(clean_chunk)
                    documents[-1]["_source"]["content_vector"] = vector
                except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                    if embed_fail_fast:
                        raise RuntimeError(
                            f"Embedding fehlgeschlagen fuer Chunk {chunk_id}: {exc}"
                        ) from exc
                    print(
                        f"  -> Warnung: Embedding fuer {chunk_id} fehlgeschlagen ({exc}). "
                        "Chunk wird ohne content_vector indexiert."
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

    embedder: OllamaEmbedder | None = None
    embedding_dims = int(args.embedding_dims)
    if args.enable_vectors:
        embedder = OllamaEmbedder(
            api_url=args.embedding_api_url,
            model=args.embedding_model,
            timeout_seconds=args.embedding_timeout,
            expected_dims=embedding_dims,
        )
        if embedding_dims <= 0:
            print("Bestimme Embedding-Dimensionen ueber Probe...")
            embedding_dims = embedder.probe_dimensions()
            embedder.expected_dims = embedding_dims
            print(f"  -> Erkannte Embedding-Dimension: {embedding_dims}")

    es = setup_elasticsearch(
        es_host=args.es_host,
        index_name=args.index,
        reset_index=args.reset_index,
        enable_vectors=args.enable_vectors,
        embedding_dims=embedding_dims,
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
                embedder=embedder,
                embed_fail_fast=args.embedding_fail_fast,
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
    if args.enable_vectors:
        print(f"Vektor-Ingestion aktiv mit Modell: {args.embedding_model}")
        print(f"Vektor-Dimensionen: {embedding_dims}")


if __name__ == "__main__":
    main()