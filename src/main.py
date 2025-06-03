from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import database
from src.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI()


app.include_router(post_router)
