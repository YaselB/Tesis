from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Chat(Base):
    __tablename__ = "chat"
    id_chat = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False)
    state = Column(String(150), default="activa")
    createdAt = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    def __init__(self, id_chat: int = None, id_user: int = None, state: str = "activa", createdAt: datetime = None):
        self.id_chat = id_chat
        self.id_user = id_user
        self.state = state
        self.createdAt = createdAt or datetime.now()