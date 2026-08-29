from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.mixins import IdIntPkMixin, TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.database.models import TreatmentPlan


class Diagnose(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.DIAGNOSE

    name: Mapped[str] = mapped_column(
        String(2048), nullable=False, index=True, unique=True
    )

    treatment_plans: Mapped[list[TreatmentPlan]] = relationship(
        back_populates="diagnose"
    )
