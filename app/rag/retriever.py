from langchain_core.retrievers import BaseRetriever
from app.rag.vector_store import get_vector_store


def get_retriever(k: int = 4) -> BaseRetriever:
    """
    Loads the persisted Chroma DB vector store and returns it as a similarity retriever.
    
    Args:
        k (int): Number of top matching document chunks to retrieve per query.
        
    Returns:
        BaseRetriever: A LangChain retriever instance ready for RAG chains.
    """
    vector_store = get_vector_store()
    
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )