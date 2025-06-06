from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import database
from src.routers.post import router as post_router


# context manager - function that does some setup and taredown and in the middle purses execution until something happens
@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()  # run the database before the fastapi app and kinda stop by yielding until fastapi wake it up
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router)
