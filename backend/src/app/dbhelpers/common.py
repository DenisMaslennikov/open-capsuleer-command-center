"""Helpers shared by two or more aggregates."""

from __future__ import annotations

from datetime import UTC, datetime


def utcnow() -> datetime:
    """Return the current time as an aware UTC datetime.

    Stored timestamps are always aware and always UTC; the interface converts to local time.
    """
    return datetime.now(tz=UTC)
