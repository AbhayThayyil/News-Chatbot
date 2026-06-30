import logging
import uuid

from app.schemas.chat import ChatResponse, Citation

logger = logging.getLogger("app")


class ChatService:
    """Generates a chat reply. Currently returns dummy data; will call the
    news retrieval + LLM pipeline in a later module."""

    def generate_reply(self, message: str, conversation_id: str | None) -> ChatResponse:
        logger.info("Generating chat reply for message: %s", message)

        return ChatResponse(
            reply=(
                f"This is a placeholder reply to: \"{message}\". "
                "Real summarization will be wired up once news retrieval and the LLM are connected."
            ),
            citations=[
                Citation(
                    title="Example News Source",
                    url="https://example.com/article",
                    source="Example News",
                )
            ],
            conversation_id=conversation_id or str(uuid.uuid4()),
        )
