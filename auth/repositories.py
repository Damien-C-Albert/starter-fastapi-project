from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from datetime import datetime, timedelta

from auth.models import Session


async def create_session(
    db: AsyncSession,
    *,
    user_id: int,
    expires_at: datetime,
    refresh_token_hash: str | None = None,
) -> Session:
    """
    Create a new session for a user in the database.
    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user for whom the session is being created.
    Returns:
        Session: The newly created session object with auto-generated fields populated.
    Raises:
        SQLAlchemyError: If there is a database error during commit or refresh.
    """
    
    session = Session(
        user_id=user_id,
        expires_at=expires_at,
        refresh_token_hash=refresh_token_hash,
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session

async def get_session_by_id(
    db: AsyncSession,
    id: int,
) -> Session | None:
    """
    Retrieve a Session from the database by their id.
    This function queries the database to find a Session with the specified id.
    It performs an asynchronous database lookup using SQLAlchemy's select statement.
    Args:
        db (AsyncSession): An async SQLAlchemy session object for database operations.
        id (int): The id of the Session to retrieve.
    Returns:
        Session | None: A Session object if a Session with the given id exists,
                     otherwise None if no matching Session is found.
    Raises:
        None: This function does not raise exceptions; it returns None for no matches.
    """
    stmt = select(Session).where(Session.id == id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()  # Return one object or None if no such user
