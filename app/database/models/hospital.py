from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.mixins import IdIntPkMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.database.models import Address, Cabinet, User


class Hospital(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.HOSPITAL

    name: Mapped[str] = mapped_column(String(256), nullable=False)

    number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    address: Mapped[Address] = relationship(back_populates="hospitals")

    address_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.ADDRESS}.id"), nullable=False
    )

    cabinets: Mapped[list[Cabinet]] = relationship(back_populates="hospital")

    users: Mapped[list[User]] = relationship("User", back_populates="hospital")

    __table_args__ = (
        UniqueConstraint(
            "address_id",
            "name",
            "number",
        ),
    )
