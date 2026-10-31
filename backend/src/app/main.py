"""Application factory and process lifespan."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import dispose_engine
from app.esi.client import EsiClient
from app.sync.runner import SyncRunner


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Own process-wide resources: the ESI HTTP session and the background sync loop."""
    settings = get_settings()
    configure_logging(settings.log_level)
    client = EsiClient.from_settings(settings)
    runner = SyncRunner(client=client, interval_seconds=settings.sync_interval_seconds)
    app.state.esi = client
    app.state.sync = runner
    await runner.start()
    try:
        yield
    finally:
        await runner.stop()
        await client.close()
        await dispose_engine()


def create_app() -> FastAPI:
    """Build the ASGI application."""
    settings = get_settings()
    app = FastAPI(
        title="OpenCapsuleerCommandCenter",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/api/docs" if settings.env != "prod" else None,
        openapi_url="/api/openapi.json",
    )
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/healthz", tags=["meta"])
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "env": settings.env}

    return app


app = create_app()
