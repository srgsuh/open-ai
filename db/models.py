from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, func
from db_connection import Base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "t_role"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

class User(Base):
    __tablename__ = "t_user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("t_role.id"), nullable=False, index=True)

    role: Mapped["Role"] = relationship()

class Request(Base):
    __tablename__ = "t_request"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("t_user.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now()
    )

    user: Mapped["User"] = relationship()