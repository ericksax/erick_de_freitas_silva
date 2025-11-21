from fastapi import APIRouter, HTTPException
import logging


from ..services.normalizer import trigger_once_normalize
from ..core.scheduler import get_scheduler


router = APIRouter()
log = logging.getLogger("api")


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/trigger")
async def trigger():
    """Manual trigger: calls scheduler to execute one collection immediately."""
    scheduler = get_scheduler()
    if not scheduler:
        raise HTTPException(status_code=500, detail="Scheduler not initialized")

    await scheduler.trigger_once()
    return {"triggered": True}
