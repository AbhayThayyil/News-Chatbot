from app.schemas.news import NewsCategory, NewsSearchRequest, TimeRange

CATEGORY_KEYWORDS: dict[NewsCategory, list[str]] = {
    "sports": ["sports news", "sports updates", "sports"],
    "technology": ["technology news", "tech news"],
    "business": ["business news", "stock market", "economy"],
    "world": ["world news", "global news"],
    "science": ["science news"],
    "health": ["health news"],
    "entertainment": ["entertainment news"],
}

TIME_KEYWORDS: dict[TimeRange, list[str]] = {
    "today": ["today", "latest", "right now"],
    "week": ["this week", "weekly", "past week"],
    "month": ["this month", "monthly", "past month"],
}


def build_news_request(message: str, max_results: int = 6) -> NewsSearchRequest:
    """Turn a free-text chat message into a structured news search request."""
    lowered = message.lower()

    category = next(
        (cat for cat, keywords in CATEGORY_KEYWORDS.items() if any(k in lowered for k in keywords)),
        None,
    )
    time_range = next(
        (tr for tr, keywords in TIME_KEYWORDS.items() if any(k in lowered for k in keywords)),
        None,
    )

    if category:
        return NewsSearchRequest(category=category, max_results=max_results)
    return NewsSearchRequest(query=message, time_range=time_range, max_results=max_results)
