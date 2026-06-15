from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class DoctorBaseSchema(BaseModel):
    pass


class DoctorUserSchema(BaseModel):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: Optional[EmailStr]
    date_of_birth: date

    model_config = ConfigDict(from_attributes=True)


class DoctorReadSchema(DoctorBaseSchema):
    id: int
    user: Optional[DoctorUserSchema]

    model_config = ConfigDict(from_attributes=True)


class AllDoctorsResponseSchema(BaseModel):
    doctors: Optional[list[DoctorReadSchema]]  # TODO data
    total: int
    limit: int
    offset: int
