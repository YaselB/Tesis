import jwt
from typing import Optional

JWT_SECRET = "super secret key for new project with the 512 bytes patreon , thanks for user my app"
JWT_ALGORITHM = "HS256"

def create_access_token(subject: str) -> str:
    payload = {
        "sub" : subject
    }
    token = jwt.encode(payload , JWT_SECRET , JWT_ALGORITHM)
    return token
def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token ,JWT_SECRET , algorithms=[JWT_ALGORITHM]) 
        return payload
    except jwt.PyJWTError:
        return None