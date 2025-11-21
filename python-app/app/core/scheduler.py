import asyncio
import logging
from typing import Optional


from .config import settings
from ..services.weather_client import WeatherClient
from ..services.normalizer import Normalizer
from ..services.publisher import Publisher


log = logging.getLogger("scheduler")


class Scheduler:
    def __init__(self):
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()
        self._client = WeatherClient(settings)
        self._normalizer = Normalizer(settings)
        self._publisher = Publisher(settings)

    async def start(self):
        log.info(
            "Starting scheduler loop with interval %s seconds",
            settings.interval_seconds,
        )
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self):
        log.info("Stopping scheduler")
        self._stop_event.set()
        if self._task:
            await self._task
        await self._publisher.close()

    async def _run_loop(self):
        await self._publisher.connect()
        while not self._stop_event.is_set():
            try:
                raw = await self._client.fetch()
                normalized = self._normalizer.normalize(raw)
                await self._publisher.publish(normalized)
                log.info("Cycle completed")
            except Exception as e:
                log.exception("Error in scheduler cycle: %s", e)
                # wait or until stop
            try:
                await asyncio.wait_for(
                    self._stop_event.wait(), timeout=settings.interval_seconds
                )
            except asyncio.TimeoutError:
                continue

    async def trigger_once(self):
        # immediate single run
        raw = await self._client.fetch()
        normalized = self._normalizer.normalize(raw)
        await self._publisher.publish(normalized)


# helper to access scheduler instance from routes
_scheduler_instance: Scheduler | None = None


def get_scheduler() -> Scheduler | None:
    global _scheduler_instance
    return _scheduler_instance


def set_scheduler(inst: Scheduler):
    global _scheduler_instance
    _scheduler_instance = inst
