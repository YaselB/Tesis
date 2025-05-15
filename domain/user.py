from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "user"
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True)
    createdAt = Column(DateTime, default=datetime.utcnow)