from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from models import User


async def create_user(
    db: AsyncSession,   # Receives session
    *,
    email: str,
    hashed_password: str,
) -> User:
    """
    Create a new user in the database.
    This coroutine function creates a new User instance with the provided email and hashed password,
    persists it to the database, and returns the created user object with all database-generated fields populated.
    Args:
        db (AsyncSession): An asynchronous SQLAlchemy database session used to interact with the database.
        email (str): The email address of the user to be created.
        hashed_password (str): The hashed password for the user account.
    Returns:
        User: The newly created User object with all fields including any database-generated identifiers.
    Raises:
        sqlalchemy.exc.IntegrityError: If a user with the given email already exists (assuming email uniqueness constraint).
    """
    user = User(
        email=email,
        hashed_password=hashed_password,
    )
    db.add(user)            # Adds object to session, No DB call yet
    await db.commit()       # INSERT happens here
    await db.refresh(user)  # Fetches DB-generated values, eg. id,defaults etc. Keep ORM object in sync
    return user

async def get_user_by_email(
    db: AsyncSession,
    email: str,
) -> User | None:
    """
    Retrieve a user from the database by their email address.
    This function queries the database to find a user with the specified email.
    It performs an asynchronous database lookup using SQLAlchemy's select statement.
    Args:
        db (AsyncSession): An async SQLAlchemy session object for database operations.
        email (str): The email address of the user to retrieve.
    Returns:
        User | None: A User object if a user with the given email exists,
                     otherwise None if no matching user is found.
    Raises:
        None: This function does not raise exceptions; it returns None for no matches.
    """
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  # Return one object or None if no such user


# Notes:
# Try flush,refresh,rollback,commit examples
