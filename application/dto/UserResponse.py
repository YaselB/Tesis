from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    id_user: int
    name: str
    email: str
    create_at: datetime
    access_token: str