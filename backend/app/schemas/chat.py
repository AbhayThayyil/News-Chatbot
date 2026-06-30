from pydantic import BaseModel, Field


class Citation(BaseModel):
    title: str
    url: str
    source: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    citations: list[Citation]
    conversation_id: str
