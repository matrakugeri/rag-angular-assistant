from typing import AsyncGenerator, List
from sqlalchemy.orm import Session

from app.models.chat import ChatMessageModel
from app.services.rag_service import RAGService


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.rag_service = RAGService()

    async def stream_and_save_chat(
        self, question: str, session_id: str
    ) -> AsyncGenerator[str, None]:
        """
        Saves the user prompt, streams RAG tokens, and persists the final assistant response.
        """
        user_message = ChatMessageModel(
            session_id=session_id,
            role="user",
            content=question
        )
        self.db.add(user_message)
        self.db.commit()

        full_response = ""

        async for token in self.rag_service.generate_stream(question):
            full_response += token
            yield token

        assistant_message = ChatMessageModel(
            session_id=session_id,
            role="assistant",
            content=full_response
        )
        self.db.add(assistant_message)
        self.db.commit()

    def get_session_history(self, session_id: str) -> List[ChatMessageModel]:
        """
        Retrieves ordered conversation history for a given session.
        """
        return (
            self.db.query(ChatMessageModel)
            .filter(ChatMessageModel.session_id == session_id)
            .order_by(ChatMessageModel.created_at.asc())
            .all()
        )