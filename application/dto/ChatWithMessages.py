from pydantic import BaseModel
from datetime import datetime
from typing import List
from application.dto.MessageResponse import MessageResponse

class ChatWithMessages(BaseModel):
    id_chat: int
    id_user: int 
    state: str
    createdAt: datetime
    messages: List[MessageResponse]