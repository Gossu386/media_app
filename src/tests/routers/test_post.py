import logging

import pytest
from httpx import AsyncClient

from src import security
from src.tests.helpers import create_comment, create_post, like_post

"""
Pytests for creating posts/comments and getting them
Using pytests.fixtures for injections called by fixture's function name
"""

logger = logging.getLogger(__name__)


@pytest.fixture()
def mock_generate_cute_creature_api(mocker):
    return mocker.patch(
        "src.tasks._generate_cute_creature_api",
        return_value={"output_url": "http://example.com/image.jpg"},
    )


@pytest.fixture()
async def created_comment(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    return await create_comment(
        "Test Comment", created_post["id"], async_client, logged_in_token
    )


@pytest.mark.anyio
async def test_create_post(
    async_client: AsyncClient, confirmed_user: dict, logged_in_token: str
):
    body = "Test Post"

    response = await async_client.post(
        "/post",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    response_data = response.json()
    assert response.status_code == 201
    assert {
        "id": 1,
        "body": body,
        "user_id": confirmed_user["id"],
        "image_url": None,
    }.items() <= response_data.items()

    assert isinstance(response_data["id"], int)
    assert isinstance(response_data["body"], str)
    assert isinstance(response_data["user_id"], int)
    assert response_data["id"] > 0


@pytest.mark.anyio
async def test_create_post_with_prompt(
    async_client: AsyncClient, logged_in_token: str, mock_generate_cute_creature_api
):
    body = "Test Post"
    response = await async_client.post(
        "/post?prompt=A cat",
        json={"body": body},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 201
    assert {
        "id": 1,
        "body": body,
        "image_url": None,
    }.items() <= response.json().items()
    mock_generate_cute_creature_api.assert_called()


@pytest.mark.anyio
async def test_create_post_expired_token(
    async_client: AsyncClient, confirmed_user: dict, mocker
):
    mocker.patch("src.security.access_token_expire_minutes", return_value=-1)
    token = security.create_access_token(confirmed_user["email"])
    response = await async_client.post(
        "/post",
        json={"body": "Test Post"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401

    response_data = response.json()
    logger.info(response_data)
    assert "detail" in response_data
    assert "Token has expired" in response_data["detail"]
    assert isinstance(response_data["detail"], str)


@pytest.mark.anyio
async def test_create_post_missing_body(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.post(
        "/post",
        json={},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )

    assert response.status_code == 422

    # Verify validation error structure
    response_data = response.json()
    assert "detail" in response_data
    assert isinstance(response_data["detail"], list)
    assert len(response_data["detail"]) > 0


@pytest.mark.anyio
async def test_like_post(
    async_client: AsyncClient, created_post: dict, logged_in_token: str
):
    response = await async_client.post(
        "/like",
        json={"post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    response_data = response.json()
    assert {
        "id": 1,
        "post_id": created_post["id"],
    }.items() <= response_data.items()
    # Verify response contains all expected fields
    assert isinstance(response_data["id"], int)
    assert isinstance(response_data["post_id"], int)
    assert isinstance(response_data["user_id"], int)
    assert response_data["id"] > 0


@pytest.mark.anyio
async def test_get_all_posts(async_client: AsyncClient, created_post: dict):
    response = await async_client.get("/post")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == [{**created_post, "likes": 0}]
    assert isinstance(response_data, list)
    assert len(response_data) == 1


@pytest.mark.anyio
@pytest.mark.parametrize(
    "sorting, expected_order",
    [
        ("new", [2, 1]),
        ("old", [1, 2]),
    ],
)
async def test_get_all_posts_sorting(
    async_client: AsyncClient,
    logged_in_token: str,
    sorting: str,
    expected_order: list[int],
):
    await create_post("Test Post 1", async_client, logged_in_token)
    await create_post("Test Post 2", async_client, logged_in_token)
    response = await async_client.get("/post", params={"sorting": sorting})
    assert response.status_code == 200

    data = response.json()
    post_ids = [post["id"] for post in data]
    assert post_ids == expected_order


@pytest.mark.anyio
async def test_get_all_posts_likes(async_client: AsyncClient, logged_in_token: str):
    await create_post("Test Post 1", async_client, logged_in_token)
    await create_post("Test Post 2", async_client, logged_in_token)
    await like_post(1, async_client, logged_in_token)
    response = await async_client.get("/post", params={"sorting": "most_likes"})
    assert response.status_code == 200

    data = response.json()
    post_ids = [post["id"] for post in data]
    expected_order = [1, 2]
    assert post_ids == expected_order


@pytest.mark.anyio
async def test_get_all_posts_wrong_sorting(
    async_client: AsyncClient, logged_in_token: str
):
    response = await async_client.get("/post", params={"sorting": "invalid_sorting"})
    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_comment(
    async_client: AsyncClient,
    created_post: dict,
    confirmed_user: dict,
    logged_in_token: str,
):
    body = "Test Comment"

    response = await async_client.post(
        "/comment",
        json={"body": body, "post_id": created_post["id"]},
        headers={"Authorization": f"Bearer {logged_in_token}"},
    )
    assert response.status_code == 201
    response_data = response.json()
    assert {
        "id": 1,
        "body": body,
        "post_id": created_post["id"],
        "user_id": confirmed_user["id"],
    }.items() <= response_data.items()
    # Verify response contains all expected fields
    assert isinstance(response_data["id"], int)
    assert isinstance(response_data["body"], str)
    assert isinstance(response_data["post_id"], int)
    assert isinstance(response_data["user_id"], int)
    assert response_data["id"] > 0


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    response_data = response.json()
    assert response.status_code == 200
    assert response_data == [created_comment]
    assert isinstance(response_data, list)
    assert len(response_data) == 1


@pytest.mark.anyio
async def test_get_comments_on_post_empty(
    async_client: AsyncClient, created_post: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code == 200

    # Verify empty list is returned
    response_data = response.json()
    assert response_data == []
    assert isinstance(response_data, list)
    assert len(response_data) == 0


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code == 200
    response_data = response.json()

    # Verify response structure has post and comments
    assert response_data == {
        "post": {**created_post, "likes": 0},
        "comments": [created_comment],
    }
    assert "post" in response_data
    assert "comments" in response_data
    assert isinstance(response_data["post"], dict)
    assert isinstance(response_data["comments"], list)
    assert response_data["post"]["id"] == created_post["id"]
    assert len(response_data["comments"]) == 1
    assert response_data["comments"][0]["id"] == created_comment["id"]


@pytest.mark.anyio
async def test_get_missing_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get("/post/2")

    assert response.status_code == 404
    # Verify error response structure and message
    response_data = response.json()
    assert "detail" in response_data
    assert response_data["detail"] == "Post not found"
    assert isinstance(response_data["detail"], str)
