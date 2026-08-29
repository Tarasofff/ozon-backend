from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
    Enum,
    UniqueConstraint,
    column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base
from app.database.models.enums import TableNames, TreatmentPlanStatus
from app.database.models.mixins import TimestampMixin, IdIntPkMixin

if TYPE_CHECKING:
    from app.database.models import Doctor, Diagnose, Patient, Session


class TreatmentPlan(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.TREATMENT_PLAN

    patient_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.PATIENT}.id"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.DOCTOR}.id"), nullable=False
    )
    diagnose_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.DIAGNOSE}.id"),
        nullable=False,
    )

    planned_session_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )

    status: Mapped[TreatmentPlanStatus] = mapped_column(
        Enum(TreatmentPlanStatus, native_enum=False),
        default=TreatmentPlanStatus.IN_PROGRESS,
        server_default=TreatmentPlanStatus.IN_PROGRESS.value,
        nullable=False,
    )

    patient: Mapped[Patient] = relationship(back_populates="treatment_plans")
    doctor: Mapped[Doctor] = relationship(back_populates="treatment_plans")
    diagnose: Mapped[Diagnose] = relationship(back_populates="treatment_plans")
    sessions: Mapped[list[Session]] = relationship(back_populates="treatment_plans")

    __table_args__ = (
        # Частичный уникальный индекс для PostgreSQL:
        # Нельзя создать 2 активных плана для одного пациента по одному диагнозу
        UniqueConstraint(
            "patient_id",
            "diagnose_id",
            name="ix_uq_active_patient_diagnose_plan",
            postgresql_where=(column("status") == TreatmentPlanStatus.IN_PROGRESS),
        ),
        CheckConstraint(
            "planned_session_count >= 0", name="ck_planned_session_count_non_negative"
        ),
    )
