from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from core.database import get_db
from core.security import decode_access_token
from auth.repositories import get_session_by_id
from users.repositories import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve the current user based on the provided OAuth2 token.
    This asynchronous function extracts the user information from the token,
    validates the session associated with the user, and returns the user object.
    Parameters:
        token (str): The OAuth2 token used for authentication, automatically
                     provided by the FastAPI dependency injection system.
        db (AsyncSession): The database session, automatically provided by
                           the FastAPI dependency injection system.
    Returns:
        User: The user object corresponding to the authenticated user.
    Raises:
        HTTPException: If the token is invalid (401) or if the session is
                       expired or inactive (401).
    """
    
    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    session_id = payload.get("sid")
    user_id = int(payload.get("sub"))

    session = await get_session_by_id(db, session_id)

    if not session or not session.is_active or session.expires_at < datetime.now(timezone.utc):
    # if not session or not session.is_active or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")

    user = await get_user_by_id(db, int(user_id))
    return user
