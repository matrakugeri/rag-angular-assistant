import os
from langchain_openai import OpenAIEmbeddings


def get_embedding_model() -> OpenAIEmbeddings:
    """
    Returns the OpenAI embedding model instance.
    Uses 'text-embedding-3-small' for optimal balance of speed and quality.
    Requires OPENAI_API_KEY set in your .env file.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set in .env")

    return OpenAIEmbeddings(
        model="text-embedding-3-small"
    )