from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from users.services import authenticate_user
from auth.repositories import create_session, get_session_by_id
from core.security import create_access_token


async def login_user(
    db: AsyncSession,
    *,
    email: str,
    password: str,
):
    """
    Authenticate a user and create an active session with an access token.
    Args:
        db: Database session object for executing queries.
        email (str): The user's email address.
        password (str): The user's password.
    Returns:
        dict: A dictionary containing:
            - access_token (str): JWT token for authenticating subsequent requests.
            - token_type (str): The token type, always "bearer".
    Raises:
        ValueError: If the user does not exist, credentials are invalid, or user is inactive.
    Notes:
        - Session expires after 1 day from creation.
        - The access token is tied to both user_id and session_id.
    """
    
    user = await authenticate_user(db, email=email, password=password)

    if not user:
        raise ValueError("Invalid email or password")
        
    if not user.is_active:
        raise ValueError("Inactive user")

    # if not user or not user.is_active:
    #     raise ValueError("Invalid credentials")

    session = await create_session(
        db,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=1),
        # expires_at=datetime.utcnow() + timedelta(days=1),
    )

    access_token = create_access_token(
        user_id=user.id,
        session_id=session.id,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

async def logout_user(
        db: AsyncSession, 
        session_id: int
):
    """
    Logs out a user by deactivating their session.
    Args:
        db: The database session used to interact with the database.
        session_id (int): The ID of the session to be logged out.
    Returns:
        None: The function modifies the session's active status in the database.
    Raises:
        Exception: If the session cannot be found or if there is an issue with the database commit.
    """

    session = await get_session_by_id(db, session_id)
    if session:
        session.is_active = False
        await db.commit()

