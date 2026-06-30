import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from xml.etree import ElementTree

import httpx
from fastapi import HTTPException

from app.schemas.news import NewsArticle, NewsSearchRequest, NewsSearchResponse
from app.utils.query_parser import build_feed_url

logger = logging.getLogger("app")

REQUEST_TIMEOUT_SECONDS = 10.0


class NewsService:
    """Fetches and normalizes articles from Google News RSS."""

    async def search(self, request: NewsSearchRequest) -> NewsSearchResponse:
        feed_url = build_feed_url(request)
        logger.info("Fetching news feed: %s", feed_url)

        xml_text = await self._fetch_feed(feed_url)
        articles = self._parse_feed(xml_text)
        articles = self._deduplicate(articles)
        articles.sort(key=lambda article: article.published_at, reverse=True)

        label = request.category or request.query or ""
        return NewsSearchResponse(query=label, articles=articles[: request.max_results])

    async def _fetch_feed(self, feed_url: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS, follow_redirects=True) as client:
                response = await client.get(feed_url)
                response.raise_for_status()
                return response.text
        except httpx.HTTPError as exc:
            logger.error("News provider request failed: %s", exc)
            raise HTTPException(status_code=502, detail="News provider unavailable") from exc

    def _parse_feed(self, xml_text: str) -> list[NewsArticle]:
        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError as exc:
            logger.error("Failed to parse news feed XML: %s", exc)
            raise HTTPException(status_code=502, detail="News provider returned an invalid response") from exc

        articles: list[NewsArticle] = []
        for item in root.findall("./channel/item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            source_el = item.find("source")
            source = source_el.text.strip() if source_el is not None and source_el.text else "Unknown"

            if not title or not link:
                continue

            if source != "Unknown" and title.endswith(f" - {source}"):
                title = title[: -(len(source) + 3)].strip()

            articles.append(
                NewsArticle(
                    title=title,
                    url=link,
                    source=source,
                    published_at=self._parse_date(item.findtext("pubDate")),
                )
            )
        return articles

    def _parse_date(self, raw: str | None) -> str:
        if not raw:
            return datetime.now(timezone.utc).isoformat()
        try:
            return parsedate_to_datetime(raw).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError):
            return datetime.now(timezone.utc).isoformat()

    def _deduplicate(self, articles: list[NewsArticle]) -> list[NewsArticle]:
        seen: set[str] = set()
        unique: list[NewsArticle] = []
        for article in articles:
            key = article.title.lower()
            if key in seen:
                continue
            seen.add(key)
            unique.append(article)
        return unique
