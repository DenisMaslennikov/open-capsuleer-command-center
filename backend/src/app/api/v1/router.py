"""Router assembly for API version 1."""

from __future__ import annotations

from fastapi import APIRouter

from app.core.config import get_settings
from app.core.scopes import SCOPE_TO_CAPABILITIES, Capability

api_router = APIRouter()


@api_router.get("/meta", tags=["meta"])
async def meta() -> dict[str, object]:
    """Report build information and the scope registry the interface draws from."""
    settings = get_settings()
    return {
        "env": settings.env,
        "esi_configured": settings.eve_sso_configured,
        "capabilities": {
            scope: sorted(cap.value for cap in caps)
            for scope, caps in SCOPE_TO_CAPABILITIES.items()
        },
        "all_capabilities": sorted(cap.value for cap in Capability),
    }
