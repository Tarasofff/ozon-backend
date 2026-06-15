from datetime import date
from typing import Optional
from pydantic import BaseModel
from .shared import BaseRead, PaginatedResponse, BaseCreate


class PatientBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    date_of_birth: date
    email: Optional[str]
    is_active: bool
    notes: Optional[str]


class PatientDiagnose(BaseCreate):
    id: int  # diagnose id
    planned_session_count: int


class PatientCreate(BaseCreate, PatientBase):
    user_id: int
    diagnose_ids: Optional[list[PatientDiagnose]]


class PatientRead(PatientBase, BaseRead):
    pass


class PatientUpdate(BaseCreate):
    first_name: str | None = None
    middle_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    date_of_birth: date | None = None
    notes: str | None = None
    is_active: bool | None = None
    email: str | None = None


class PaginatedPatientsResponse(PaginatedResponse[PatientRead]):
    pass
