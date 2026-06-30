from functools import lru_cache

from app.services.chat_service import ChatService
from app.services.news_service import NewsService


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()


@lru_cache
def get_news_service() -> NewsService:
    return NewsService()
