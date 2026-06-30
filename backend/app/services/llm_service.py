import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.utils.retry import is_retryable_http_error, retry_async

logger = logging.getLogger("app")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
REQUEST_TIMEOUT_SECONDS = 20.0


class LLMService:
    """Calls the Groq chat completions API to generate summaries."""

    async def complete(self, messages: list[dict[str, str]]) -> str:
        if not settings.groq_api_key:
            raise HTTPException(status_code=500, detail="LLM provider is not configured")

        payload = {
            "model": settings.groq_model,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 600,
        }
        headers = {"Authorization": f"Bearer {settings.groq_api_key}"}

        async def attempt() -> httpx.Response:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                response = await client.post(GROQ_CHAT_URL, json=payload, headers=headers)
                response.raise_for_status()
                return response

        try:
            response = await retry_async(
                attempt, attempts=2, base_delay=1.0, should_retry=is_retryable_http_error, label="Groq completion"
            )
        except httpx.HTTPStatusError as exc:
            logger.error("Groq API error after retries: %s - %s", exc.response.status_code, exc.response.text)
            raise HTTPException(status_code=502, detail="LLM provider request failed") from exc
        except httpx.HTTPError as exc:
            logger.error("Groq API request failed after retries: %s", exc)
            raise HTTPException(status_code=502, detail="LLM provider unavailable") from exc

        try:
            return response.json()["choices"][0]["message"]["content"].strip()
        except (KeyError, IndexError, ValueError) as exc:
            logger.error("Unexpected Groq response shape: %s", exc)
            raise HTTPException(status_code=502, detail="LLM provider returned an unexpected response") from exc
