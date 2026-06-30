import logging
import uuid

from app.schemas.chat import ChatResponse, Citation
from app.services.llm_service import LLMService
from app.services.news_service import NewsService
from app.utils.intent_parser import build_news_request
from app.utils.prompt_builder import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger("app")


class ChatService:
    """Orchestrates news retrieval and LLM summarization for a chat reply."""

    def __init__(self, news_service: NewsService, llm_service: LLMService) -> None:
        self._news_service = news_service
        self._llm_service = llm_service

    async def generate_reply(self, message: str, conversation_id: str | None) -> ChatResponse:
        logger.info("Generating chat reply for message: %s", message)

        news_request = build_news_request(message)
        news_response = await self._news_service.search(news_request)

        user_prompt = build_user_prompt(message, news_response.articles)
        reply = await self._llm_service.complete(SYSTEM_PROMPT, user_prompt)

        citations = [
            Citation(title=article.title, url=article.url, source=article.source)
            for article in news_response.articles
        ]

        return ChatResponse(
            reply=reply,
            citations=citations,
            conversation_id=conversation_id or str(uuid.uuid4()),
        )
