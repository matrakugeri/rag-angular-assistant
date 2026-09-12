from app.rag.loader import load_documents_from_web
from app.rag.splitter import split_documents
from app.rag.vector_store import create_vector_store

def main():
    # 1. Scrape web pages
    docs = load_documents_from_web()

    # 2. Split scraped HTML text into chunks
    chunks = split_documents(docs)

    # 3. Store embeddings into Chroma DB
    create_vector_store(chunks)

if __name__ == "__main__":
    main()