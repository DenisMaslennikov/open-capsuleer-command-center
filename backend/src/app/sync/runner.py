"""Background synchronisation loop."""

from __future__ import annotations

import asyncio
import logging

from app.esi.client import EsiClient

log = logging.getLogger(__name__)


class SyncRunner:
    """Periodically refreshes character data into the database.

    Tasks are registered by feature slices; the runner only owns scheduling, cancellation
    and failure isolation, so a failing task never stops the loop.
    """

    def __init__(self, client: EsiClient, interval_seconds: int) -> None:
        self._client = client
        self._interval = interval_seconds
        self._task: asyncio.Task[None] | None = None
        self._stop = asyncio.Event()

    async def start(self) -> None:
        """Start the loop if it is not running already."""
        if self._task is None:
            self._task = asyncio.create_task(self._run(), name="sync-loop")

    async def stop(self) -> None:
        """Signal the loop to stop and wait for it to finish."""
        self._stop.set()
        if self._task is not None:
            await self._task
            self._task = None

    async def _run(self) -> None:
        while not self._stop.is_set():
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=self._interval)
            except TimeoutError:
                log.debug("sync tick")
