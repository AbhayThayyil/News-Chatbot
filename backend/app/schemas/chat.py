from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    url: str
    source: str
    published_at: str
    confidence: float = Field(ge=0.0, le=1.0)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = Field(default=None, min_length=1)


class ChatResponse(BaseModel):
    reply: str
    citations: list[Citation]
    conversation_id: str
