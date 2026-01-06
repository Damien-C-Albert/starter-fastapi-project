from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from .schemas import LoginRequest, LoginResponse
from . import services


router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        user = await services.login_user(
            db,
            email=payload.email,
            password=payload.password,
        )
        return user

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )
