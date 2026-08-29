from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.mixins import IdIntPkMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.database.models import Session, Cabinet


class Post(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.POST

    number: Mapped[int] = mapped_column(Integer, nullable=False)

    cabinet: Mapped[Cabinet] = relationship(back_populates="posts")

    cabinet_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.CABINET}.id"), nullable=False
    )

    sessions: Mapped[list[Session]] = relationship(back_populates="post")

    __table_args__ = (
        UniqueConstraint(
            "cabinet_id",
            "number",
        ),
    )
