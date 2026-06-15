from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import String
from app.db.models.base import Base
from app.db.models.mixins import IdIntPkMixin, TimestampMixin
from app.db.table_names import TableNames
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.db.models import PatientDoctorDiagnose


class Diagnose(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.DIAGNOSE

    name: Mapped[str] = mapped_column(
        String(2048), nullable=False, index=True, unique=True
    )

    patient_doctor_diagnose: Mapped[list[PatientDoctorDiagnose]] = relationship(
        back_populates="diagnose"
    )
