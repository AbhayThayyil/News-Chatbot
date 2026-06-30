import logging
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.chat import Citation

logger = logging.getLogger("app")

HISTORY_LIMIT = 6
TITLE_MAX_LENGTH = 60


class ConversationService:
    """Persists conversations and messages, and provides recent history for context building."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_or_create(self, conversation_id: str | None, first_message: str) -> Conversation:
        if conversation_id:
            existing = self._db.get(Conversation, conversation_id)
            if existing:
                return existing

        title = first_message.strip()[:TITLE_MAX_LENGTH]
        conversation = Conversation(id=conversation_id or None, title=title)
        self._db.add(conversation)
        self._db.commit()
        self._db.refresh(conversation)
        return conversation

    def get_recent_messages(self, conversation_id: str, limit: int = HISTORY_LIMIT) -> list[Message]:
        conversation = self._db.get(Conversation, conversation_id)
        if not conversation:
            return []
        return conversation.messages[-limit:]

    def get_last_citations(self, conversation_id: str) -> list[Citation] | None:
        messages = self.get_recent_messages(conversation_id, limit=HISTORY_LIMIT)
        for message in reversed(messages):
            if message.role == "assistant" and message.citations:
                return [Citation.model_validate(citation) for citation in message.citations]
        return None

    def add_message(
        self, conversation_id: str, role: str, content: str, citations: list[Citation] | None = None
    ) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            citations=[c.model_dump() for c in citations] if citations else None,
        )
        self._db.add(message)

        conversation = self._db.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.now(timezone.utc)

        self._db.commit()
        self._db.refresh(message)
        return message

    def list_conversations(self) -> list[Conversation]:
        return (
            self._db.query(Conversation)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self._db.get(Conversation, conversation_id)

    def rename(self, conversation_id: str, title: str) -> Conversation | None:
        conversation = self._db.get(Conversation, conversation_id)
        if not conversation:
            return None
        conversation.title = title
        self._db.commit()
        self._db.refresh(conversation)
        return conversation

    def delete(self, conversation_id: str) -> bool:
        conversation = self._db.get(Conversation, conversation_id)
        if not conversation:
            return False
        self._db.delete(conversation)
        self._db.commit()
        return True
