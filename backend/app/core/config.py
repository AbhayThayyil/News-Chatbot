from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI News Chatbot API"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:5173"]
    log_level: str = "INFO"

    database_url: str = "sqlite:///./chatbot.db"

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
