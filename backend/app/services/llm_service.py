import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger("app")

GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
REQUEST_TIMEOUT_SECONDS = 20.0


class LLMService:
    """Calls the Groq chat completions API to generate summaries."""

    async def complete(self, system_prompt: str, user_prompt: str) -> str:
        if not settings.groq_api_key:
            raise HTTPException(status_code=500, detail="LLM provider is not configured")

        payload = {
            "model": settings.groq_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 600,
        }
        headers = {"Authorization": f"Bearer {settings.groq_api_key}"}

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                response = await client.post(GROQ_CHAT_URL, json=payload, headers=headers)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("Groq API error: %s - %s", exc.response.status_code, exc.response.text)
            raise HTTPException(status_code=502, detail="LLM provider request failed") from exc
        except httpx.HTTPError as exc:
            logger.error("Groq API request failed: %s", exc)
            raise HTTPException(status_code=502, detail="LLM provider unavailable") from exc

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
