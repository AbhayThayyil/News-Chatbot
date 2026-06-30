from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.chat_service import ChatService
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.news_service import NewsService


@lru_cache
def get_news_service() -> NewsService:
    return NewsService()


@lru_cache
def get_llm_service() -> LLMService:
    return LLMService()


def get_conversation_service(db: Session = Depends(get_db)) -> ConversationService:
    return ConversationService(db)


def get_chat_service(
    news_service: NewsService = Depends(get_news_service),
    llm_service: LLMService = Depends(get_llm_service),
    conversation_service: ConversationService = Depends(get_conversation_service),
) -> ChatService:
    return ChatService(news_service, llm_service, conversation_service)
