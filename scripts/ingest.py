import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.loader import scrape_angular_docs
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store


def main():
    print("Starting Web Crawling & Ingestion for Angular Docs...")

    raw_docs = scrape_angular_docs()
    print(f"Fetched {len(raw_docs)} document pages.")

    if not raw_docs:
        print("No documents were found during crawl.")
        return

    print("Splitting documents into semantic chunks...")
    chunks = split_documents(raw_docs)
    print(f"Generated {len(chunks)} text chunks.")

    print("Generating embeddings and building Chroma DB index...")
    create_vector_store(chunks)

    print("\nIngestion complete! Chroma DB successfully created at ./data/chroma_db")


if __name__ == "__main__":
    main()