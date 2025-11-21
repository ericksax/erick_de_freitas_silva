import asyncio
import logging
from fastapi import FastAPI
from dotenv import load_dotenv


from .api.routes import router
from .core.scheduler import Scheduler
from .core.config import settings
from .core.logger import configure_logging


load_dotenv()
configure_logging()
logger = logging.getLogger("main")


app = FastAPI(title="Weather Producer")
app.include_router(router)


scheduler: Scheduler | None = None


@app.on_event("startup")
async def startup_event():
    global scheduler
    logger.info("Starting application")
    scheduler = Scheduler()
    await scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    global scheduler
    logger.info("Shutting down application")
    if scheduler:
        await scheduler.stop()
