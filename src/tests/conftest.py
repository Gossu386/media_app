from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.routers.post import comment_table, post_table

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
def client() -> Generator:
    yield TestClient(app)

@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield

@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac