from urllib.parse import quote

from app.schemas.news import NewsSearchRequest

GOOGLE_NEWS_BASE = "https://news.google.com/rss"

CATEGORY_TOPICS = {
    "world": "WORLD",
    "business": "BUSINESS",
    "technology": "TECHNOLOGY",
    "entertainment": "ENTERTAINMENT",
    "science": "SCIENCE",
    "sports": "SPORTS",
    "health": "HEALTH",
}

TIME_RANGE_QUALIFIERS = {
    "today": "when:1d",
    "week": "when:7d",
    "month": "when:1m",
}


def build_feed_url(request: NewsSearchRequest) -> str:
    """Translate a search request into a Google News RSS feed URL."""
    if request.category:
        topic = CATEGORY_TOPICS[request.category]
        return f"{GOOGLE_NEWS_BASE}/headlines/section/topic/{topic}?hl=en-US&gl=US&ceid=US:en"

    query = request.query.strip() if request.query else ""
    if request.time_range:
        query = f"{query} {TIME_RANGE_QUALIFIERS[request.time_range]}"

    return f"{GOOGLE_NEWS_BASE}/search?q={quote(query)}&hl=en-US&gl=US&ceid=US:en"
