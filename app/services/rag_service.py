import logging
from typing import AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.rag.retriever import get_retriever

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.retriever = get_retriever(k=4)

        self.llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0.2,
            streaming=True
        )

        system_prompt = (
            "You are an expert Angular AI assistant specializing in modern Angular practices "
            "(Signals, Control Flow syntax, RxJS, Component Architecture, and Dependency Injection).\n"
            "Use the retrieved documentation context below to answer the user's question accurately.\n"
            "If you do not know the answer or if the context does not contain enough information, state that clearly.\n\n"
            "Context:\n{context}"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])

        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    async def generate_stream(self, question: str) -> AsyncGenerator[str, None]:
        """
        Asynchronously yields generated tokens from the LLM stream.
        """
        try:
            async for chunk in self.rag_chain.astream({"input": question}):
                if "answer" in chunk:
                    yield chunk["answer"]
        except Exception as e:
            logger.error(f"Error in RAGService streaming generation: {e}")
            yield f"\n[Error generating response: {str(e)}]"