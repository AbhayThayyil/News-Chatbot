from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI News Chatbot API"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:5173"]
    log_level: str = "INFO"

    groq_api_key: str = ""
    groq_model: str = "llama-3.1-8b-instant"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
