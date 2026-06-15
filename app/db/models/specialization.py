from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from app.db.models.base import Base
from app.db.models.mixins import IdIntPkMixin, TimestampMixin
from app.db.table_names import TableNames
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Doctor


class Specialization(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.SPECIALIZATION

    name: Mapped[str] = mapped_column(String(256), nullable=False)

    doctor: Mapped[list[Doctor]] = relationship(back_populates="specialization")

    __table_args__ = (
        UniqueConstraint(
            "name",
        ),
    )
