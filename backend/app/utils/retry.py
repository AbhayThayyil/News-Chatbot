import asyncio
import logging
from typing import Awaitable, Callable, TypeVar

import httpx

logger = logging.getLogger("app")

T = TypeVar("T")


def is_retryable_http_error(exc: Exception) -> bool:
    """Network failures and timeouts are always worth retrying. A 5xx or 429
    response might clear up on retry; other 4xx responses won't."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= 500 or exc.response.status_code == 429
    return isinstance(exc, httpx.RequestError)


async def retry_async(
    func: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    base_delay: float = 0.5,
    should_retry: Callable[[Exception], bool] = lambda _exc: True,
    label: str = "operation",
) -> T:
    last_exc: Exception | None = None

    for attempt in range(1, attempts + 1):
        try:
            return await func()
        except Exception as exc:  # noqa: BLE001 — re-raised below if not retryable
            if not should_retry(exc) or attempt == attempts:
                raise
            last_exc = exc
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                "%s failed (attempt %d/%d): %s — retrying in %.1fs",
                label,
                attempt,
                attempts,
                exc,
                delay,
            )
            await asyncio.sleep(delay)

    assert last_exc is not None  # unreachable: loop always returns or raises
    raise last_exc
