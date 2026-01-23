import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from src.configs.logging_config import configure_logging
from src.database import database
from src.routers.post import router as post_router
from src.routers.user import router as user_router

logger = logging.getLogger(__name__)


# context manager - function that does some setup and taredown and in the middle purses execution until something happens
@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()  # run the database before the fastapi app and kinda stop by yielding until fastapi wake it up
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(post_router)
app.include_router(user_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HttpException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)
