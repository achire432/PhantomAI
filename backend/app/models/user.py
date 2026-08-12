from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database.database import Base


class User(Base):
    __tablename__ = "users"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    # IMPORTANT:
    # This field must NEVER be returned by the database explorer.
    # It contains the password hash, not the user's plaintext password.
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # ============================================================
    # STAFF / AUTHORIZATION
    # ============================================================

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="user",
        index=True
    )

    organization: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        index=True
    )

    is_staff: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        index=True
    )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    settings = relationship(
        "UserSettings",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )