from typing import List
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.chat import ChatRequest, ChatMessageResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    POST /api/chat/stream
    Streams text tokens directly back to the Angular client.
    """
    service = ChatService(db=db)
    session_id = payload.session_id or "default_session"

    return StreamingResponse(
        service.stream_and_save_chat(
            question=payload.message,
            session_id=session_id
        ),
        media_type="text/plain"
    )


@router.get("/history/{session_id}", response_model=List[ChatMessageResponse])
def get_chat_history(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    GET /api/chat/history/{session_id}
    Retrieves stored message history.
    """
    service = ChatService(db=db)
    return service.get_session_history(session_id=session_id)

