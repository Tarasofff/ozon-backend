from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Date, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from app.db.models.base import Base
from app.db.models.mixins import IdIntPkMixin, TimestampMixin
from app.db.table_names import TableNames


if TYPE_CHECKING:
    from app.db.models import Nurse, Role, Doctor


class User(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.USER

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)

    middle_name: Mapped[str] = mapped_column(String(64), nullable=False)

    last_name: Mapped[str] = mapped_column(String(64), nullable=False)

    phone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(String(length=320), nullable=True)

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, server_default=text("true")
    )

    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    nurse: Mapped[Nurse] = relationship(back_populates="user")

    doctor: Mapped[Doctor] = relationship(back_populates="user")

    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.ROLE}.id"), nullable=False
    )

    role: Mapped[Role] = relationship(back_populates="user")
