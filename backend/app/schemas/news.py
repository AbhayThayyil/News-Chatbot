from pydantic import BaseModel, Field


class NewsSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=200)
    max_results: int = Field(default=5, ge=1, le=20)


class NewsArticle(BaseModel):
    title: str
    url: str
    source: str
    published_at: str


class NewsSearchResponse(BaseModel):
    query: str
    articles: list[NewsArticle]
