import os
import pymupdf4llm
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Konfiguration
PDF_PATH = "../data/dsa_regelwerk.pdf"
INDEX_NAME = "lara_documents"
ES_HOST = "http://localhost:9200"

def setup_elasticsearch():
    """Verbindet sich mit ES und erstellt den Index mit deutschen Settings."""
    es = Elasticsearch(ES_HOST)
    
    # Warte, bis ES verfügbar ist
    if not es.ping():
        raise ConnectionError("Elasticsearch ist nicht erreichbar. Läuft Docker?")

    # Index Mapping: Sagt ES, wie die Daten aussehen (z.B. deutscher Text)
    mapping = {
        "mappings": {
            "properties": {
                "source": {"type": "keyword"}, # Der Dateiname (für Filter)
                "page": {"type": "integer"},   # Die Seitenzahl
                "content": {
                    "type": "text", 
                    "analyzer": "german"       # Wichtig für DSA (Stichwort: Umlaute & Grammatik!)
                }
            }
        }
    }
    
    # Index löschen, falls er schon existiert (gut fürs Prototyping)
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"Alten Index '{INDEX_NAME}' gelöscht.")
        
    es.indices.create(index=INDEX_NAME, body=mapping)
    print(f"Index '{INDEX_NAME}' bereit.")
    return es

def extract_and_chunk_pdf():
    """Liest das PDF in Markdown und zerteilt es in kleine Chunks."""
    print(f"Lese PDF: {PDF_PATH} (Das kann kurz dauern...)")
    
    # pymupdf4llm macht die Magie: Wandelt PDF zu Markdown um (page_chunks=True trennt pro Seite)
    md_pages = pymupdf4llm.to_markdown(PDF_PATH, page_chunks=True)
    
    # Wir zerteilen den Text in sinnvolle Agenten-Häppchen
    # chunk_size=1000 Zeichen (gut für kleine lokale LLMs)
    # chunk_overlap=200 verhindert, dass Sätze/Tabellenangaben mittendrin zerrissen werden
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    documents = []
    
    for page_data in md_pages:
        page_num = page_data.get("metadata", {}).get("page", 0) + 1
        text = page_data.get("text", "")
        
        # Text zerteilen
        chunks = text_splitter.split_text(text)
        
        for chunk in chunks:
            # Ein Dokument-Objekt für Elasticsearch vorbereiten
            doc = {
                "_index": INDEX_NAME,
                "_source": {
                    "source": "dsa_regelwerk",
                    "page": page_num,
                    "content": chunk
                }
            }
            documents.append(doc)
            
    print(f"PDF extrahiert in {len(documents)} Text-Chunks.")
    return documents

def main():
    try:
        es = setup_elasticsearch()
        docs = extract_and_chunk_pdf()
        
        print("Sende Daten an Elasticsearch...")
        # Bulk-API: Sendet alle Chunks extrem schnell auf einmal an die Datenbank
        success, failed = bulk(es, docs)
        print(f"Fertig! Erfolgreich indexiert: {success} Chunks.")
        if failed:
            print(f"Fehler bei {len(failed)} Chunks.")
            
    except Exception as e:
        print(f"Fehler beim Indexieren: {e}")

if __name__ == "__main__":
    main()