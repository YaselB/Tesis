from fastapi import Depends , HTTPException , status
from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from application.auth.jwt_utils import decode_access_token

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    subject = decode_access_token(token)
    if subject is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Token inválido o expirado")
    return subject
    