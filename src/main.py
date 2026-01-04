from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth
from src.api.rooms import router as router_rooms
from src.api.bookings import router as router_bookings
from src.api.facilities import router as router_facilities
from src.api.images import router as router_images
from src.config import settings
from src.init import redis_manager

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis=redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


if settings.MODE == "TEST":
    FastAPICache.init(RedisBackend(redis=redis_manager.redis), prefix="fastapi-cache")

app = FastAPI(lifespan=lifespan)

app.include_router(router_auth)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_bookings)
app.include_router(router_facilities)
app.include_router(router_images)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
