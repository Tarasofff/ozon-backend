from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr
from .shared import BaseRead, PaginatedResponse, BaseCreate
from app.schemas.shared.types import (
    FirstNameStr,
    LastNameStr,
    PatronymicStr,
    PhoneStr,
)


class PatientBase(BaseModel):
    first_name: FirstNameStr
    patronymic: PatronymicStr
    last_name: LastNameStr
    phone: PhoneStr
    date_of_birth: date
    email: EmailStr | None = None
    is_active: bool
    notes: str | None = None


class PatientDiagnose(BaseCreate):
    id: int  # diagnose id
    planned_session_count: int


class PatientCreate(BaseCreate, PatientBase):
    user_id: int
    diagnose_ids: Optional[list[PatientDiagnose]]


class PatientRead(PatientBase, BaseRead):
    pass


class PaginatedPatientsResponse(PaginatedResponse[PatientRead]):
    pass
