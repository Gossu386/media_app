import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

os.environ["ENV_STATE"] = "test"
from src.database import database # noqa: E402
from src.main import app  # noqa: E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(autouse=True)
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=client.base_url) as ac:
        yield ac


"""
This module sets up pytest fixtures for testing the FastAPI application. It includes configurations for 
the test environment, database connection management, and HTTP client utilities for both synchronous 
and asynchronous testing.

Modules Imported:
- os: Used to set environment variables for the test environment.
- typing: Provides type hints for generator and asynchronous generator functions.
- pytest: A testing framework used to define fixtures and manage test cases.
- fastapi.testclient.TestClient: A synchronous test client for testing FastAPI applications.
- httpx: Provides an asynchronous HTTP client for testing FastAPI applications.
- src.database: The database connection module for the application.
- src.main: The main FastAPI application instance.

Environment Variables:
- ENV_STATE: Set to "test" to configure the application for the test environment.

Fixtures:
1. anyio_backend:
    - Scope: session
    - Purpose: Specifies the backend for AnyIO, which is used for asynchronous testing. 
      In this case, it is set to "asyncio".

2. client:
    - Scope: function (default)
    - Purpose: Provides a synchronous `TestClient` instance for testing the FastAPI application.
    - Autouse: Enabled, so it is automatically used in all test cases.

3. db:
    - Scope: function (default)
    - Purpose: Manages the lifecycle of the database connection during tests. 
      It connects to the database before a test starts and disconnects after the test ends.
    - Autouse: Enabled, so it is automatically used in all test cases.

4. async_client:
    - Scope: function (default)
    - Purpose: Provides an asynchronous `AsyncClient` instance for testing the FastAPI application.
      It uses `ASGITransport` to simulate requests to the application.

Logic Flow:
- The `ENV_STATE` environment variable is set to "test" to ensure the application runs in a test-specific configuration.
- The `client` fixture initializes a synchronous test client for making HTTP requests to the FastAPI app.
- The `db` fixture ensures the database connection is properly managed during tests, preventing resource leaks.
- The `async_client` fixture provides an asynchronous test client for scenarios requiring async HTTP requests.
"""