from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base
from app.database.models.enums import TableNames, SessionStatus
from app.database.models.mixins import TimestampMixin, IdIntPkMixin
from app.utils.utils import enum_values

if TYPE_CHECKING:
    from app.database.models import Nurse, Post, TreatmentPlan


class Session(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.SESSION

    notes: Mapped[str | None] = mapped_column(String(1024), nullable=True)

    session_duration: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Session duration in seconds"
    )

    status: Mapped[SessionStatus] = mapped_column(
        Enum(SessionStatus, native_enum=False, values_callable=enum_values),
        default=SessionStatus.PLANNED,
        server_default=SessionStatus.PLANNED.value,
        nullable=False,
        index=True,
    )

    ozone_concentration: Mapped[float] = mapped_column(
        Float, nullable=False, comment="mg/l"
    )

    nurse_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.NURSE}.id"), nullable=True
    )

    nurse: Mapped[Nurse] = relationship(back_populates="sessions")

    treatment_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.TREATMENT_PLAN}.id"), nullable=False
    )

    treatment_plans: Mapped[TreatmentPlan] = relationship(back_populates="sessions")

    post: Mapped[Post] = relationship(back_populates="sessions")

    post_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(f"{TableNames.POST}.id"), nullable=False
    )
