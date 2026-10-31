"""Configuration contract."""

from __future__ import annotations

import pytest

from app.core.config import Settings


def test_settings_require_explicit_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://user:pass@localhost:5432/db")
    settings = Settings(_env_file=None)
    assert settings.database_url.endswith("/db")


def test_eve_sso_is_not_configured_without_credentials() -> None:
    settings = Settings(_env_file=None, eve_client_id="", eve_client_secret="")
    assert settings.eve_sso_configured is False


def test_eve_sso_is_configured_when_all_three_values_are_present() -> None:
    settings = Settings(
        _env_file=None,
        eve_client_id="id",
        eve_client_secret="secret",
        eve_callback_url="https://example.invalid/callback",
    )
    assert settings.eve_sso_configured is True
