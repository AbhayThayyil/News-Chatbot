import json

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI News Chatbot API"
    environment: str = "development"
    log_level: str = "INFO"

    # Plain string, not list[str] — pydantic-settings JSON-decodes complex
    # (list/dict) env values automatically, and strict JSON is easy to
    # mangle typing into a dashboard's env var field. Accept either a JSON
    # array or a comma-separated string and parse it ourselves below.
    cors_origins: str = "http://localhost:5173"

    database_url: str = "sqlite:///./chatbot.db"

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    @property
    def cors_origins_list(self) -> list[str]:
        value = self.cors_origins.strip()
        if value.startswith("["):
            return json.loads(value)
        return [origin.strip() for origin in value.split(",") if origin.strip()]

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
