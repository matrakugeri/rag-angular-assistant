import os
import logging
from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.rag.embeddings import get_embedding_model

logger = logging.getLogger(__name__)

CHROMA_PATH = os.path.abspath("./data/chroma_db")
COLLECTION_NAME = "angular_docs"


def create_vector_store(documents: List[Document]) -> Chroma:
    """
    Creates a new Chroma vector store from document chunks,
    generates embeddings, and persists the index to disk.
    """
    if not documents:
        raise ValueError("Cannot create vector store with an empty list of documents.")

    os.makedirs(os.path.dirname(CHROMA_PATH), exist_ok=True)
    embeddings = get_embedding_model()

    logger.info(f"Embedding {len(documents)} document chunks into Chroma DB at: {CHROMA_PATH}")

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH
    )

    logger.info("Chroma DB successfully created.")
    return vector_store


def get_vector_store() -> Chroma:
    """
    Loads and returns the existing persisted Chroma DB instance from disk.
    """
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(
            f"Vector store directory '{CHROMA_PATH}' was not found. "
            
        )

    embeddings = get_embedding_model()

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH
    )