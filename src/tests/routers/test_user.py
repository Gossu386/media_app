import pytest
from httpx import AsyncClient


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/register", json={"email": email, "password": password}
    )


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(async_client, "test@example.net", "1234")
    assert response.status_code == 201
    assert "User created" in response.json()["detail"]
    # Verify response body structure
    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], str)


@pytest.mark.anyio
async def test_register_user_already_exists(
    async_client: AsyncClient, registered_user: dict
):
    response = await register_user(
        async_client, registered_user["email"], registered_user["password"]
    )
    assert "already exists" in response.json()["detail"]
    assert response.status_code == 400
    # Verify detailed error message content
    assert "An user with that email already exists" == response.json()["detail"]
    assert "detail" in response.json()


@pytest.mark.anyio
async def test_login_user_not_exists(async_client: AsyncClient):
    response = await async_client.post(
        "/token", json={"email": "test@example.net", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    # Verify error response structure and content
    assert "detail" in response.json()
    assert "Could not validate credentials" in response.json()["detail"]


@pytest.mark.anyio
async def test_login_user(async_client: AsyncClient, registered_user: dict):
    response = await async_client.post(
        "/token",
        json={
            "email": registered_user["email"],
            "password": registered_user["password"],
        },
    )
    assert response.status_code == 200
    # Verify token response structure
    response_data = response.json()
    assert "access_token" in response_data
    assert "token_type" in response_data
    assert response_data["token_type"] == "bearer"
    assert isinstance(response_data["access_token"], str)
    assert len(response_data["access_token"]) > 0
