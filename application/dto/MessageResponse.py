from pydantic import BaseModel
from datetime import datetime

class MessageResponse(BaseModel):
    id_message: int 
    id_chat: int
    content: str
    response: str
    type: str
    createdAt: datetime