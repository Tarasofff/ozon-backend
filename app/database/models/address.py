from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint
from app.database.models.base import Base
from app.database.models.mixins import IdIntPkMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.enums import TableNames

if TYPE_CHECKING:
    from app.database.models import Hospital


class Address(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.ADDRESS

    country_name: Mapped[str] = mapped_column(String(256), nullable=False)

    city_name: Mapped[str] = mapped_column(String(256), nullable=False)

    street_name: Mapped[str] = mapped_column(String(256), nullable=False)

    building_number: Mapped[str] = mapped_column(String(256), nullable=False)

    hospitals: Mapped[list[Hospital]] = relationship(back_populates="address")

    __table_args__ = (
        UniqueConstraint(
            "country_name",
            "city_name",
            "street_name",
            "building_number",
        ),
    )
