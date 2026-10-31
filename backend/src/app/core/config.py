"""Process configuration read from the environment."""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings.

    Values come from the environment or from a `.env` file next to the process working
    directory. Secrets never have defaults: a missing key fails at start-up rather than
    silently disabling a feature.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "dev"
    log_level: str = "INFO"

    database_url: str = "postgresql+psycopg://occc:occc@db:5432/occc"

    eve_client_id: str = ""
    eve_client_secret: str = ""
    eve_callback_url: str = ""

    secret_key: str = Field(default="", min_length=0)
    token_encryption_key: str = ""

    esi_compatibility_date: str = "2026-10-31"
    sync_interval_seconds: int = 900
    esi_error_budget_floor: int = 20

    @property
    def eve_sso_configured(self) -> bool:
        """Whether EVE application credentials are present."""
        return bool(self.eve_client_id and self.eve_client_secret and self.eve_callback_url)


@lru_cache
def get_settings() -> Settings:
    """Return the process-wide settings instance."""
    return Settings()
