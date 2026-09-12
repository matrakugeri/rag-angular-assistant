from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database.db import Base

class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(50), index=True)
    role = Column(String(20))
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"


class ChatMessageResponse(BaseModel):
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True