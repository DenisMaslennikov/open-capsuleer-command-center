"""FastAPI dependencies shared by routers."""

from __future__ import annotations

from collections.abc import AsyncIterator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session_factory
from app.esi.client import EsiClient


async def db_session() -> AsyncIterator[AsyncSession]:
    """Yield a session for one request and roll back unfinished work on exit."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def esi_client(request: Request) -> EsiClient:
    """Return the process-wide ESI client created during start-up."""
    return request.app.state.esi


EsiDep = Depends(esi_client)
SessionDep = Depends(db_session)
