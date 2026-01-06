from sqlalchemy.ext.asyncio import AsyncSession

from users.services import authenticate_user


async def login_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
):
    user = await authenticate_user(
        db,
        email=email,
        password=password,
    )

    if not user:
        raise ValueError("Invalid email or password")

    if not user.is_active:
        raise ValueError("Inactive user")

    return user
