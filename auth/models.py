from sqlalchemy import ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

from core.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    refresh_token_hash: Mapped[str | None] = mapped_column(String(255))
    expires_at: Mapped[datetime]

    is_active: Mapped[bool] = mapped_column(default=True)
    # created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
