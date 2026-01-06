from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from datetime import datetime, timedelta

from auth.models import Session


async def create_session(
    db: AsyncSession,
    *,
    user_id: int,
):
    session = Session(user_id=user_id)
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session
