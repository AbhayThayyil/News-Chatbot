from pydantic import BaseModel, Field, field_validator


class Citation(BaseModel):
    title: str
    url: str
    source: str
    published_at: str
    confidence: float = Field(ge=0.0, le=1.0)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = Field(default=None, min_length=1)

    @field_validator("message")
    @classmethod
    def reject_blank_message(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Message cannot be empty or whitespace only")
        return stripped


class ChatResponse(BaseModel):
    reply: str
    citations: list[Citation]
    conversation_id: str
