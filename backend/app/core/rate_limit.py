import time
from collections import defaultdict

from fastapi import HTTPException, Request


class RateLimiter:
    """Simple in-memory fixed-window rate limiter, keyed per client IP.

    Single-process only, same caveat as TTLCache — fine for one backend
    instance; would need a shared store (e.g. Redis) across replicas.
    """

    def __init__(self, max_requests: int, window_seconds: float) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._hits: dict[str, list[float]] = defaultdict(list)

    def check(self, client_id: str) -> None:
        now = time.monotonic()
        window_start = now - self._window_seconds
        hits = self._hits[client_id]

        while hits and hits[0] < window_start:
            hits.pop(0)

        if len(hits) >= self._max_requests:
            raise HTTPException(status_code=429, detail="Too many requests — please slow down and try again shortly")

        hits.append(now)


chat_rate_limiter = RateLimiter(max_requests=20, window_seconds=60)


def enforce_chat_rate_limit(request: Request) -> None:
    client_id = request.client.host if request.client else "unknown"
    chat_rate_limiter.check(client_id)
