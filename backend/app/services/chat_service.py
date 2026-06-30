import logging

from app.schemas.chat import ChatResponse
from app.services.conversation_service import ConversationService
from app.services.llm_service import LLMService
from app.services.news_service import NewsService
from app.utils.citation_builder import build_citations
from app.utils.intent_parser import build_news_request, is_follow_up
from app.utils.prompt_builder import SYSTEM_PROMPT, build_user_prompt

logger = logging.getLogger("app")


class ChatService:
    """Orchestrates conversation history, news retrieval, and LLM summarization."""

    def __init__(
        self,
        news_service: NewsService,
        llm_service: LLMService,
        conversation_service: ConversationService,
    ) -> None:
        self._news_service = news_service
        self._llm_service = llm_service
        self._conversations = conversation_service

    async def generate_reply(self, message: str, conversation_id: str | None) -> ChatResponse:
        logger.info("Generating chat reply for message: %s", message)

        conversation = self._conversations.get_or_create(conversation_id, message)
        history = self._conversations.get_recent_messages(conversation.id)
        previous_citations = self._conversations.get_last_citations(conversation.id)

        if is_follow_up(message, has_history=bool(history)) and previous_citations:
            citations = previous_citations
            logger.info("Treating message as a follow-up; reusing %d prior citations", len(citations))
        else:
            news_request = build_news_request(message)
            news_response = await self._news_service.search(news_request)
            citations = build_citations(news_response.articles)

        llm_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for past in history:
            llm_messages.append({"role": past.role, "content": past.content})
        llm_messages.append({"role": "user", "content": build_user_prompt(message, citations)})

        reply = await self._llm_service.complete(llm_messages)

        self._conversations.add_message(conversation.id, "user", message)
        self._conversations.add_message(conversation.id, "assistant", reply, citations=citations)

        return ChatResponse(reply=reply, citations=citations, conversation_id=conversation.id)
