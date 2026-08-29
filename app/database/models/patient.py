from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from datetime import date
from sqlalchemy import Boolean, String, Date, true
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.models.base import Base
from app.database.models.enums.table_names import TableNames
from app.database.models.mixins import TimestampMixin, IdIntPkMixin

if TYPE_CHECKING:
    from app.database.models import TreatmentPlan


class Patient(IdIntPkMixin, TimestampMixin, Base):
    __tablename__ = TableNames.PATIENT

    first_name: Mapped[str] = mapped_column(String(64), nullable=False)

    patronymic: Mapped[str] = mapped_column(String(64), nullable=True)

    last_name: Mapped[str] = mapped_column(String(64), nullable=False)

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)

    email: Mapped[Optional[str]] = mapped_column(String(length=320), nullable=True)

    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False, server_default=true()
    )

    treatment_plans: Mapped[list[TreatmentPlan]] = relationship(back_populates="patient")
