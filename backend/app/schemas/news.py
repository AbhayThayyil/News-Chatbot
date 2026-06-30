from typing import Literal

from pydantic import BaseModel, Field, model_validator

NewsCategory = Literal["world", "business", "technology", "entertainment", "science", "sports", "health"]
TimeRange = Literal["today", "week", "month"]


class NewsSearchRequest(BaseModel):
    query: str | None = Field(default=None, min_length=1, max_length=200)
    category: NewsCategory | None = None
    time_range: TimeRange | None = None
    max_results: int = Field(default=10, ge=1, le=30)

    @model_validator(mode="after")
    def require_query_or_category(self) -> "NewsSearchRequest":
        if not self.query and not self.category:
            raise ValueError("Provide either 'query' or 'category'")
        return self


class NewsArticle(BaseModel):
    title: str
    url: str
    source: str
    published_at: str


class NewsSearchResponse(BaseModel):
    query: str
    articles: list[NewsArticle]
