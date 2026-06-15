from __future__ import annotations
from typing import TYPE_CHECKING

from datetime import date
from sqlalchemy import Boolean, String, Date, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.models.base import Base
from app.db.table_names import TableNames
from app.db.models.mixins import TimestampMixin, IdIntPkMixin

if TYPE_CHECKING:
    from app.db.models import PatientDoctorDiagnose


class Patient(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.PATIENT

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)

    middle_name: Mapped[str] = mapped_column(String(64), nullable=False)

    last_name: Mapped[str] = mapped_column(String(64), nullable=False)

    phone: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True,
        index=True,
    )

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    email: Mapped[str] = mapped_column(String(length=320), nullable=True)

    notes: Mapped[str] = mapped_column(String(1024), nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, server_default=text("true")
    )

    patient_doctor_diagnose: Mapped[list[PatientDoctorDiagnose]] = relationship(
        back_populates="patient"
    )
