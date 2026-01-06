from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from users import services
from users.schemas import UserCreate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user in the system.
    This endpoint creates a new user account with the provided email and password.
    Args:
        payload (UserCreate): Request body containing user registration details
            (email and password).
        db (AsyncSession): Database session dependency for executing queries.
            Defaults to get_db() dependency.
    Returns:
        User: The newly created user object with user details.
    Raises:
        HTTPException: With status code 409 CONFLICT if the email already exists
            in the system or other validation errors occur.
    """
    
    try:
        user = await services.register_user(
            db,
            email=payload.email,
            password=payload.password,
        )
        return user

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )