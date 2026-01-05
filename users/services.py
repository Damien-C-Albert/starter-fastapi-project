from sqlalchemy.ext.asyncio import AsyncSession

from users.repositories import get_user_by_email, create_user
from core.security import hash_password, verify_password


async def register_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
):
    """
    Register a new user with the provided email and password.
    This function creates a new user account after validating that the email
    is not already registered in the system. The password is hashed before
    storage for security purposes.
    Args:
        db (AsyncSession): The asynchronous database session for querying and creating records.
        email (str): The email address for the new user account.
        password (str): The plaintext password for the new user account.
    Returns:
        User: The newly created user object with hashed password.
    Raises:
        ValueError: If a user with the provided email already exists in the database.
    """

    existing_user = await get_user_by_email(db, email)

    if existing_user:
        raise ValueError("User with this email already exists")

    hashed_pw = hash_password(password)

    user = await create_user(
        db,
        email=email,
        hashed_password=hashed_pw,
    )

    return user

async def authenticate_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
):
    """
    Authenticate a user by email and password.
    This function retrieves a user from the database by email and verifies
    the provided password against the stored hashed password. If the user
    is found and the password is correct, the user object is returned.
    Otherwise, None is returned.
    Args:
        db (AsyncSession): The asynchronous database session.
        email (str): The email address of the user to authenticate.
        password (str): The plain text password to verify.
    Returns:
        User | None: The authenticated user object if credentials are valid,
                     otherwise None.
    """
    
    user = await get_user_by_email(db, email)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
