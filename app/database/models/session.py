from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, false, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.mixins import TimestampMixin, IdIntPkMixin

if TYPE_CHECKING:
    from app.database.models import Nurse, Post, TreatmentPlan


class Session(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.SESSION

    notes: Mapped[str] = mapped_column(String(1024), nullable=True)

    session_duration: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Session duration seconds"
    )

    ozone_concentration: Mapped[float] = mapped_column(
        Float, nullable=False, comment="mg/l"
    )
    # ???
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=false()
    )

    nurse_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.NURSE}.id"), nullable=True
    )

    nurse: Mapped[Nurse] = relationship(back_populates="sessions")

    treatment_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.TREATMENT_PLAN}.id"), nullable=False
    )

    treatment_plan: Mapped[TreatmentPlan] = relationship(back_populates="session")

    post: Mapped[Post] = relationship(back_populates="session")

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.POST}.id"), nullable=False
    )
