from __future__ import annotations
from typing import TYPE_CHECKING, List

from sqlalchemy import CheckConstraint, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base
from app.db.table_names import TableNames
from app.db.models.mixins import TimestampMixin, IdIntPkMixin


if TYPE_CHECKING:
    from app.db.models import Doctor, Diagnose, Patient, Session


class PatientDoctorDiagnose(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.PATIENT_DOCTOR_DIAGNOSE

    patient_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.PATIENT}.id"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.DOCTOR}.id"), nullable=False
    )
    diagnose_id: Mapped[int] = mapped_column(
        ForeignKey(f"{TableNames.DIAGNOSE}.id"),
        nullable=True,
    )

    planned_session_count: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0, server_default="0"
    )

    patient: Mapped[Patient] = relationship(back_populates="patient_doctor_diagnose")
    doctor: Mapped[Doctor] = relationship(back_populates="patient_doctor_diagnose")
    diagnose: Mapped[Diagnose] = relationship(back_populates="patient_doctor_diagnose")
    session: Mapped[List[Session]] = relationship(
        back_populates="patient_doctor_diagnose"
    )

    __table_args__ = (
        UniqueConstraint(
            "patient_id",
            "doctor_id",
            "diagnose_id",
        ),
        CheckConstraint(
            "planned_session_count >= 0", name="ck_planned_session_count_non_negative"
        ),
    )
