from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from app.db.models.base import Base
from app.db.models.mixins import IdIntPkMixin, TimestampMixin
from app.db.table_names import TableNames
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import Hospital


class Address(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.ADDRESS

    country_name: Mapped[str] = mapped_column(String(256), nullable=False)

    city_name: Mapped[str] = mapped_column(String(256), nullable=False)

    street_name: Mapped[str] = mapped_column(String(256), nullable=False)

    building_number: Mapped[str] = mapped_column(String(256), nullable=False)

    postal_code: Mapped[str] = mapped_column(String(256), nullable=False)

    hospital: Mapped[list[Hospital]] = relationship(back_populates="address")

    __table_args__ = (
        UniqueConstraint(
            "country_name",
            "city_name",
            "street_name",
            "building_number",
        ),
    )
