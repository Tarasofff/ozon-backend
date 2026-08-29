from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String, Date, true, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.enums.user_role import UserRole
from app.database.models.mixins import IdIntPkMixin, TimestampMixin

if TYPE_CHECKING:
    from app.database.models import Hospital


# JTI
class User(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.USER

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)

    last_name: Mapped[str] = mapped_column(String(64), nullable=False)

    patronymic: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[Optional[str]] = mapped_column(String(length=320), nullable=True)

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, server_default=true()
    )

    password_hash: Mapped[str] = mapped_column(String(length=255), nullable=False)

    hospital_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.HOSPITAL}.id"), nullable=False
    )

    hospital: Mapped[Hospital] = relationship("Hospital", back_populates="users")

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, native_enum=False), nullable=False
    )

    __mapper_args__ = {
        "polymorphic_on": "role",
    }
