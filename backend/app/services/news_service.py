import logging

from app.schemas.news import NewsArticle, NewsSearchResponse

logger = logging.getLogger("app")


class NewsService:
    """Searches for news articles. Currently returns dummy data; will call a
    real news provider (e.g. Google News RSS, GNews) in a later module."""

    def search(self, query: str, max_results: int) -> NewsSearchResponse:
        logger.info("Searching news for query: %s (max_results=%d)", query, max_results)

        dummy_articles = [
            NewsArticle(
                title=f"Placeholder headline {i + 1} about '{query}'",
                url=f"https://example.com/news/{i + 1}",
                source="Example News",
                published_at="2026-06-30T00:00:00Z",
            )
            for i in range(max_results)
        ]

        return NewsSearchResponse(query=query, articles=dummy_articles)
