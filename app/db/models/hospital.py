from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from app.db.models.base import Base
from app.db.models.mixins import IdIntPkMixin, TimestampMixin
from app.db.table_names import TableNames
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Address, Cabinet


# TODO doctor & nurse
class Hospital(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.HOSPITAL

    name: Mapped[str] = mapped_column(String(256), nullable=False)

    number: Mapped[int] = mapped_column(Integer, nullable=True)

    address: Mapped[Address] = relationship(back_populates="hospital")

    address_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.ADDRESS}.id"), nullable=False
    )

    cabinet: Mapped[list[Cabinet]] = relationship(back_populates="hospital")

    __table_args__ = (
        UniqueConstraint(
            "address_id",
            "name",
            "number",
        ),
    )
