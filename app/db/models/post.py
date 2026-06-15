from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from app.db.models.base import Base
from app.db.models.mixins import IdIntPkMixin, TimestampMixin
from app.db.table_names import TableNames
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from app.db.models import Session, Cabinet


class Post(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.POST

    number: Mapped[int] = mapped_column(Integer, nullable=False)

    cabinet: Mapped[Cabinet] = relationship(back_populates="post")

    cabinet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.CABINET}.id"), nullable=False
    )

    session: Mapped[list[Session]] = relationship(back_populates="post")

    __table_args__ = (
        UniqueConstraint(
            "cabinet_id",
            "number",
        ),
    )
