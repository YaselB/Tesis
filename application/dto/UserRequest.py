from pydantic import BaseModel

class UserRequest(BaseModel):
    email: str
    name: str