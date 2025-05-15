from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    id_chat: int