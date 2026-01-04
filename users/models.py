from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    """
    User model representing a user account in the system.
    Attributes:
        id (int): Primary key identifier for the user, auto-incremented.
        email (str): Unique email address of the user (max 255 characters).
            Indexed for faster query lookups by email.
        hashed_password (str): Bcrypt hashed password for secure storage (max 255 characters).
        is_active (bool): Flag indicating whether the user account is active.
            Defaults to True when a new user is created.
    Notes:
        The `index=True` on the email field creates a database index, which optimizes
        query performance when filtering or searching users by email address. This is
        especially useful for login operations and duplicate email checks, as indexed
        columns allow the database to locate rows faster without scanning the entire table.
    """
