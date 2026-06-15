from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseSchema):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    phone: str


class NurseSchema(BaseSchema):
    id: int
    user: UserSchema


class CabinetSchema(BaseSchema):
    id: int
    number: str


class PostSchema(BaseSchema):
    id: int
    number: int
    cabinet: CabinetSchema


class SessionSchema(BaseSchema):
    id: int
    notes: Optional[str]
    session_duration_ms: int
    created_at: datetime
    updated_at: datetime
    ozone_concentration: float
    is_active: bool
    post: PostSchema
    nurse: Optional[NurseSchema]


class PatientSessionListSchema(BaseSchema):
    session: Optional[List[SessionSchema]]


class DiagnoseSchema(BaseSchema):
    id: int
    name: str


class DoctorSchema(BaseSchema):
    id: int
    user: UserSchema


class PatientDoctorDiagnoseSchema(BaseSchema):
    id: int
    doctor: DoctorSchema
    diagnose: DiagnoseSchema
    planned_session_count: int


class AddressSchema(BaseSchema):
    id: int
    country_name: str
    city_name: str
    street_name: str
    building_number: str
    postal_code: str


class HospitalSchema(BaseSchema):
    id: int
    name: str
    number: Optional[int]
    address: AddressSchema


class PatientSchema(BaseSchema):
    id: int
    first_name: str
    middle_name: Optional[str]
    last_name: str
    phone: str
    email: Optional[str]
    date_of_birth: date
    is_active: bool
    notes: Optional[str]


class PatientReportSchema(PatientSessionListSchema):
    patient: PatientSchema
    hospital: HospitalSchema
    doctor: DoctorSchema
    diagnose: DiagnoseSchema
    planned_session_count: int
