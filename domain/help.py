from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from .base import Base

class Help(Base):
    __tablename__ = "help"
    id_help = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(String(150), nullable=False)
    category = Column(String(150))
    def __init__(self, id_help: int = None, title: str = None, content: str = None, category: str = None):
        self.id_help = id_help
        self.title = title
        self.content = content
        self.category = category