from pydantic import BaseModel

class FAQItem(BaseModel):
    question: str
    count: int