from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.mixins import IdIntPkMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.database.models import Hospital, Post


class Cabinet(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.CABINET

    number: Mapped[str] = mapped_column(String(256), nullable=False)

    hospital: Mapped[Hospital] = relationship(back_populates="cabinets")

    hospital_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.HOSPITAL}.id"), nullable=False
    )

    posts: Mapped[list[Post]] = relationship(back_populates="cabinet")

    __table_args__ = (
        UniqueConstraint(
            "hospital_id",
            "number",
        ),
    )
