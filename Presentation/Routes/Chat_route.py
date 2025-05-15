from email.policy import HTTP
from typing import List
from fastapi import APIRouter , HTTPException , Depends, Request
from pydantic import BaseModel
from application.Services.Chat_Service import ChatService
from application.auth.dependencies import get_current_user
from application.dto.ChatWithMessages import ChatWithMessages
from application.dto.FAQItem import FAQItem
from application.dto.QuestionRequest import QuestionRequest
from application.Services.FAQService import FAQService
from infrastructure.user_repository import DATABASE_URL

router = APIRouter()

@router.post("/ask")
async def preguntar(
    data: QuestionRequest,
    request: Request,
    current_user: str = Depends(get_current_user)
):
    chat_service = request.app.state.chat_service
    try:
        return {"response": chat_service.answer(data.question, data.id_chat)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post("/create_new_chat/{id_user}" )
async def create_new_chat( id_user: int, current_user: str = Depends(get_current_user)):
    chat_service = request.app.state.chat_service
    try:
        chat = chat_service.create_new_chat(id_user = id_user)
        return chat
    except Exception as e:
        raise HTTPException(status_code = 400 , detail = str(e))
@router.get("/get_chat_by_id/{chat_id}" , response_model = ChatWithMessages)
async def get_chat(chat_id: int , current_user: str = Depends(get_current_user)):
    chat_service = request.app.state.chat_service
    try:
        return chat_service.get_chat_by_id(chat_id)
    except Exception as e:
        raise HTTPException(status_code = 404 , detail = str(e))
@router.delete("/delete_chat/{chat_id}")
async def delete_chat(chat_id: int, current_user: str = Depends(get_current_user)):
    chat_service = request.app.state.chat_service
    try:
        result = chat_service.delete_chat_by_id(chat_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.get("/top", response_model=List[FAQItem])
def top_faqs(
    limit: int = 10,
    threshold: float = 0.3,
    current_user: str = Depends(get_current_user)
):
    svc = FAQService(db_url=DATABASE_URL)
    return svc.top_n_faqs(n=limit, eps=threshold)