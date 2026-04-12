import logging
from json import JSONDecodeError

import httpx
from databases import Database

from src.config import config
from src.database import post_table

logger = logging.getLogger(__name__)


class APIResponseError(Exception):
    pass


async def send_simple_email(to: str, subject: str, body: str):
    logger.debug(f"Sending email to '{to[:3]}' with subject '{subject[:20]}'")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://api.mailgun.net/v3/{config.MAILGUN_DOMAIN}/messages",
                auth=("api", config.MAILGUN_API_KEY),
                data={
                    "from": f"Media App <mailgun@{config.MAILGUN_DOMAIN}>",
                    "to": [to],
                    "subject": subject,
                    "text": body,
                },
            )
            response.raise_for_status()
            logger.debug(response.content)
            return response
        except httpx.HTTPStatusError as err:
            raise APIResponseError(
                f"API request failed with status {err.response.status_code}"
            ) from err


async def send_user_registration_email(email: str, confirmation_url: str):
    return await send_simple_email(
        email,
        "Successfully signed up",
        (
            f"Hi {email}! You have signed up to Media App."
            " Please confirm your email by clicking "
            f" the following link: {confirmation_url}"
        ),
    )


async def _generate_cute_creature_api(prompt: str):
    logger.debug(f"Generating cute creature with prompt: '{prompt[:20]}'")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.deepai.org/api/cute-creature-generator",
                data={"text": prompt},
                headers={"api-key": config.DEEPAI_API_KEY},
                timeout=60,
            )
            logger.debug(response)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as err:
            raise APIResponseError(
                f"API request failed with status {err.response.status_code}"
            ) from err
        except (JSONDecodeError, TypeError) as err:
            raise APIResponseError("Failed to parse API response") from err


async def generate_and_add_to_post(
    email: str,
    post_id: int,
    post_url: str,
    database: Database,
    prompt: str = "a cute creature with big eyes and a small body",
):
    try:
        response = await _generate_cute_creature_api(prompt)
    except APIResponseError as err:
        return await send_simple_email(
            email,
            "Failed to generate image",
            (
                f"Hi {email}! We failed to generate an image for your post at {post_url}"
                f" due to an error: {err}",
            ),
        )
    logger.debug("Connecting to database to update post")

    query = (
        post_table.update()
        .where(post_table.c.id == post_id)
        .values(image_url=response["output_url"])
    )

    logger.debug(query)

    await database.execute(query)
    logger.debug("Database connection in background task closed")

    await send_simple_email(
        email,
        "Your image is ready",
        (
            f"Hi {email}! Your image for the post at {post_url} is ready. "
            f"You can view it here: {response['output_url']}"
        ),
    )
    return response
