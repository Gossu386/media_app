import logging

from fastapi import APIRouter, HTTPException, status

from src.database import database, user_table
from src.models.user import UserIn
from src.security import get_password_hash, get_user, authenticate_user, create_access_token

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An user with that email already exists",
        )

    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User created"}

@router.post("/token")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(email=user.email)
    return {"access_token": access_token, "token_type": "bearer"}