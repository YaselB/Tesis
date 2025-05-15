from sqlalchemy import Column, Integer, String, DateTime, ForeignKey , Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from .base import Base


class Message(Base):
    __tablename__ = "message"
    id_message = Column(Integer, primary_key=True, autoincrement=True)
    id_chat = Column(Integer, ForeignKey("chat.id_chat"), nullable=False)
    content = Column(String(1000))
    response = Column(Text)
    type = Column(String(150), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)

    chat = relationship("Chat")

    def __init__(self, id_message: int = None, id_chat: int = None, content: str = None,response: str =None , type: str = None, createdAt: datetime = None):
        self.id_message = id_message
        self.id_chat = id_chat
        self.content = content
        self.response = response
        self.type = type
        self.createdAt = createdAt or datetime.now()