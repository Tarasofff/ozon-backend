from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.utils.utils import DateParser


class PatientBaseSchema(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    date_of_birth: date
    email: Optional[str]
    is_active: Optional[bool] = None
    notes: Optional[str]


class PatientDiagnose(BaseModel):
    id: int

    planned_session_count: int


class PatientCreateSchema(PatientBaseSchema, DateParser):
    user_id: int
    diagnose_ids: Optional[list[PatientDiagnose]]

    model_config = ConfigDict(strict=True)


class PatientReadSchema(PatientBaseSchema):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class PatientUpdateSchema(BaseModel, DateParser):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    date_of_birth: Optional[date]
    notes: Optional[str]
    is_active: Optional[bool]
    email: Optional[str]

    model_config = ConfigDict(strict=True)


class PatientsResponseSchema(BaseModel):
    data: Optional[list[PatientReadSchema]]
    total: int
    limit: int
    offset: int
