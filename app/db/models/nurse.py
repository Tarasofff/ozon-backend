from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.table_names import TableNames
from app.db.models.base import Base
from app.db.models.mixins import TimestampMixin, IdIntPkMixin

if TYPE_CHECKING:
    from app.db.models import Session, User


class Nurse(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.NURSE

    session: Mapped[list[Session]] = relationship(back_populates="nurse")

    user: Mapped[User] = relationship(back_populates="nurse")

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.USER}.id"), nullable=False
    )
