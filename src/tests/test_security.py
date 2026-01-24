import pytest
from jose import jwt

from src import security


def test_access_token():
    assert security.access_token_expire_minutes() == 30


def test_create_access_token():
    token = security.create_access_token("123")
    decoded_token = jwt.decode(
        token, key=security.SECRET_KEY, algorithms=[security.ALGORITHM]
    )
    assert {"sub": "123"}.items() <= decoded_token.items()
    # Verify token contains expiration and is valid
    assert "exp" in decoded_token
    assert isinstance(decoded_token["exp"], int)
    assert decoded_token["exp"] > 0


def test_password_hashes():
    password = "password"
    hashed = security.get_password_hash(password)
    assert security.verify_password(password, hashed)
    # Verify hash is different from plain password and is secure
    assert hashed != password
    assert len(hashed) > len(password)
    assert hashed.startswith("$2b$")  # bcrypt hash prefix
    # Verify wrong password doesn't verify
    assert not security.verify_password("wrongpassword", hashed)


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])

    assert user.email == registered_user["email"]
    # Verify user object has all required fields
    assert hasattr(user, "id")
    assert hasattr(user, "email")
    assert hasattr(user, "password")
    assert user.id == registered_user["id"]
    assert isinstance(user.id, int)
    assert user.id > 0
    assert isinstance(user.email, str)
    assert isinstance(user.password, str)


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("test@example.com")
    assert user is None


@pytest.mark.anyio
async def test_authenticate_user(registered_user: dict):
    user = await security.authenticate_user(
        registered_user["email"], registered_user["password"]
    )

    assert user.email == registered_user["email"]
    # Verify authenticated user has complete information
    assert hasattr(user, "id")
    assert user.id == registered_user["id"]
    assert isinstance(user.id, int)
    assert user.id > 0
    assert isinstance(user.email, str)
    assert isinstance(user.password, str)


@pytest.mark.anyio
async def test_authenticate_user_not_found():
    with pytest.raises(security.HTTPException) as exc_info:
        await security.authenticate_user("test@example.com", "wrongpassword")
    # Verify exception details
    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(security.HTTPException) as exc_info:
        await security.authenticate_user(registered_user["email"], "wrongpassword")
    # Verify exception details for wrong password
    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = security.create_access_token(registered_user["email"])
    user = await security.get_current_user(token)
    assert user.email == registered_user["email"]
    # Verify current user has complete information
    assert hasattr(user, "id")
    assert user.id == registered_user["id"]
    assert isinstance(user.email, str)
    assert "@" in user.email


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(security.HTTPException) as exc_info:
        await security.get_current_user("invalid token")
    # Verify exception details for invalid token
    assert exc_info.value.status_code == 401
    assert "Could not validate credentials" in exc_info.value.detail
