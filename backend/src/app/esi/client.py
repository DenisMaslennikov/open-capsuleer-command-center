"""Single outbound boundary to the EVE Swagger Interface."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import aiohttp

from app.core.config import Settings
from app.core.errors import EsiUnavailable

log = logging.getLogger(__name__)

ESI_BASE = "https://esi.evetech.net"
ERROR_BUDGET_FLOOR = 20


@dataclass(slots=True)
class EsiResponse:
    """A cached response: body, ETag and expiry, or a not-modified marker."""

    status: int
    payload: Any | None
    etag: str | None
    expires: str | None

    @property
    def not_modified(self) -> bool:
        """Whether the server answered with 304 and the stored payload must be reused."""
        return self.status == 304


class EsiClient:
    """HTTP client that owns the ESI session, the error budget and conditional caching.

    The instance is created once per process; callers never build their own session.
    """

    def __init__(self, session: aiohttp.ClientSession, compatibility_date: str) -> None:
        self._session = session
        self._compatibility_date = compatibility_date

    @classmethod
    def from_settings(cls, settings: Settings) -> EsiClient:
        """Build the client from process settings."""
        session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30, connect=10),
            headers={
                "User-Agent": "OpenCapsuleerCommandCenter/0.1",
                "X-Compatibility-Date": settings.esi_compatibility_date,
                "Accept": "application/json",
            },
        )
        return cls(session=session, compatibility_date=settings.esi_compatibility_date)

    async def close(self) -> None:
        """Close the underlying connection pool."""
        await self._session.close()

    async def get_json(
        self,
        path: str,
        *,
        access_token: str | None = None,
        params: dict[str, Any] | None = None,
        etag: str | None = None,
    ) -> EsiResponse:
        """Perform a conditional GET against ESI.

        Args:
            path: Route beginning with a slash, without the base host.
            access_token: Bearer token for authenticated routes.
            params: Query parameters.
            etag: Previously stored ETag; a 304 answer means the stored body is still valid.

        Returns:
            Parsed body with cache metadata, or a 304 marker.

        Raises:
            EsiUnavailable: On exhausted error budget, rate limiting or a transport failure.
        """
        url = f"{ESI_BASE}{path}"
        if params:
            url = f"{url}?{urlencode(params)}"
        headers = {"If-None-Match": etag} if etag else {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        try:
            async with self._session.get(url, headers=headers) as response:
                self._check_budget(response)
                if response.status == 304:
                    return EsiResponse(304, None, etag, response.headers.get("Expires"))
                if response.status in (420, 429):
                    raise EsiUnavailable(f"rate limited on {path}")
                if response.status >= 500:
                    raise EsiUnavailable(f"upstream error {response.status} on {path}")
                payload = await response.json(content_type=None)
                return EsiResponse(
                    status=response.status,
                    payload=payload,
                    etag=response.headers.get("ETag"),
                    expires=response.headers.get("Expires"),
                )
        except aiohttp.ClientError as exc:
            raise EsiUnavailable(f"transport failure on {path}: {exc}") from exc

    @staticmethod
    def _check_budget(response: aiohttp.ClientResponse) -> None:
        remaining = response.headers.get("X-ESI-Error-Limit-Remain")
        if remaining is not None and remaining.isdigit():
            if int(remaining) <= ERROR_BUDGET_FLOOR:
                raise EsiUnavailable("ESI error budget is nearly exhausted")
