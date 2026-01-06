from sqlalchemy import ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from core.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)
