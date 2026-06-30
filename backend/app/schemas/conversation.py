from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.chat import Citation


class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role: str
    content: str
    citations: list[Citation] | None
    created_at: datetime


class ConversationSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    updated_at: datetime


class ConversationDetail(ConversationSummary):
    messages: list[MessageOut]


class RenameConversationRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
