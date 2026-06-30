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

NEW_TOPIC_SIGNALS = [
    "latest",
    "news about",
    "news on",
    "what's happening",
    "whats happening",
    "today's",
    "update on",
    "search for",
]

FOLLOW_UP_MAX_WORDS = 12


def is_follow_up(message: str, has_history: bool) -> bool:
    """Heuristic: a short message in an existing conversation that doesn't
    explicitly ask for fresh news is treated as a follow-up on the articles
    already shown, rather than triggering a new search."""
    if not has_history:
        return False

    lowered = message.lower()
    if any(signal in lowered for signal in NEW_TOPIC_SIGNALS):
        return False

    return len(message.split()) <= FOLLOW_UP_MAX_WORDS


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
