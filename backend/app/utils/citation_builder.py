from datetime import datetime, timezone
from typing import Protocol

from app.schemas.chat import Citation

RECENCY_FULL_CONFIDENCE_HOURS = 24
RECENCY_FLOOR_HOURS = 24 * 7
RANK_MIN_SCORE = 0.6
CONFIDENCE_FLOOR = 0.5


class _Article(Protocol):
    title: str
    url: str
    source: str
    published_at: str


def _recency_score(published_at: str) -> float:
    try:
        published = datetime.fromisoformat(published_at)
    except ValueError:
        return RANK_MIN_SCORE

    age_hours = (datetime.now(timezone.utc) - published).total_seconds() / 3600
    if age_hours <= RECENCY_FULL_CONFIDENCE_HOURS:
        return 1.0
    if age_hours >= RECENCY_FLOOR_HOURS:
        return RANK_MIN_SCORE

    span = RECENCY_FLOOR_HOURS - RECENCY_FULL_CONFIDENCE_HOURS
    decay = (age_hours - RECENCY_FULL_CONFIDENCE_HOURS) / span
    return 1.0 - decay * (1.0 - RANK_MIN_SCORE)


def build_citations(articles: list[_Article]) -> list[Citation]:
    """Build citations with a confidence score.

    This confidence is a heuristic proxy — an average of the article's
    position in the result list (earlier = more likely relevant to the
    query) and how recent it is. It is NOT a measure of whether the LLM
    actually grounded a specific claim in that specific article; true
    per-claim attribution would require the model to cite its sources
    during generation (e.g. function calling), which is a meaningfully
    larger feature than this heuristic.
    """
    total = len(articles)
    citations = []
    for index, article in enumerate(articles):
        rank_score = 1.0 - (index / max(total, 1)) * (1.0 - RANK_MIN_SCORE)
        recency_score = _recency_score(article.published_at)
        confidence = max(CONFIDENCE_FLOOR, min(1.0, round((rank_score + recency_score) / 2, 2)))

        citations.append(
            Citation(
                title=article.title,
                url=article.url,
                source=article.source,
                published_at=article.published_at,
                confidence=confidence,
            )
        )
    return citations
