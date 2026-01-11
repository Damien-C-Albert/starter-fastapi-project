from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from .schemas import LoginRequest, LoginResponse, TokenResponse
from . import services


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Handles user login by validating credentials and returning a user token.
    Args:
        payload (LoginRequest): The login request containing user credentials.
        db (AsyncSession, optional): The database session dependency. Defaults to the result of get_db.
    Returns:
        str: A user token if the login is successful.
    Raises:
        HTTPException: If the login fails due to invalid credentials, a 401 UNAUTHORIZED error is raised with a detailed message.
    """
    
    try:
        user_token = await services.login_user(
            db,
            email=payload.email,
            password=payload.password,
        )
        return user_token

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
