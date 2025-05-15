from datetime import datetime
from fastapi import APIRouter  , HTTPException
from application.Services.User_Service import UserService
from application.auth.jwt_utils import create_access_token
from application.dto.UserRequest import UserRequest
from application.dto.UserResponse import UserResponse
router = APIRouter(prefix="/users" , tags=["users"])


@router.post("/create_user" , response_model = UserResponse)
async def Create_user(data: UserRequest):
    try:
        user = UserService.create_user_application(data.name , data.email)
        token = create_access_token(subject=str(data.email))
        return {
            "id_user": user.id_user,
            "name": user.name,
            "email": user.email,
            "create_at": user.createdAt,
            "access_token": token
        }
    except Exception as e:
        raise HTTPException(status_code = 400 , detail = str(e))
@router.post("/login", response_model = UserResponse)
async def login(email: str):
    try:
        user = UserService.login(email = email)
        token = create_access_token(subject = str(email))
        return {
            "id_user" : user.id_user,
            "name" : user.name,
            "email" : user.email,
            "create_at" : user.createdAt ,
            "access_token" : token
        }
    except Exception as e:
        raise HTTPException(status_code = 404 , detail = str(e))