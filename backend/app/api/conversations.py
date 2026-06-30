from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_conversation_service
from app.schemas.conversation import ConversationDetail, ConversationSummary, RenameConversationRequest
from app.services.conversation_service import ConversationService

router = APIRouter(tags=["conversations"])


@router.get("/conversations", response_model=list[ConversationSummary])
def list_conversations(
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> list[ConversationSummary]:
    return conversation_service.list_conversations()


@router.get("/conversations/{conversation_id}", response_model=ConversationDetail)
def get_conversation(
    conversation_id: str, conversation_service: ConversationService = Depends(get_conversation_service)
) -> ConversationDetail:
    conversation = conversation_service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.patch("/conversations/{conversation_id}", response_model=ConversationSummary)
def rename_conversation(
    conversation_id: str,
    request: RenameConversationRequest,
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> ConversationSummary:
    conversation = conversation_service.rename(conversation_id, request.title)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.delete("/conversations/{conversation_id}", status_code=204)
def delete_conversation(
    conversation_id: str, conversation_service: ConversationService = Depends(get_conversation_service)
) -> None:
    deleted = conversation_service.delete(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
