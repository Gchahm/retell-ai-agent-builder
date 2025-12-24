from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database (Supabase PostgreSQL)
    database_url: str = "postgresql://postgres:password@localhost:5432/postgres"

    # API Keys (structure only for MVP)
    retell_api_key: str = "mock_key"
    openai_api_key: str = "mock_key"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True

    # Webhook
    webhook_base_url: str = "http://localhost:8000"

    # Dispatch phone number for emergency call transfers
    dispatch_phone_number: str = "+1234567890"

    @property
    def webhook_url(self) -> str:
        """Full webhook URL for Retell."""
        return f"{self.webhook_base_url}/api/webhooks/retell"


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
