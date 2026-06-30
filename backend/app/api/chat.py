from fastapi import APIRouter, Depends

from app.core.dependencies import get_chat_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest, chat_service: ChatService = Depends(get_chat_service)
) -> ChatResponse:
    return await chat_service.generate_reply(request.message, request.conversation_id)
