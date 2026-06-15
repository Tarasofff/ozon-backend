from typing import Optional
from pydantic import BaseModel, ConfigDict


class DoctorSpecializationBaseSchema(BaseModel):
    pass


class DoctorSpecializationReadSchema(DoctorSpecializationBaseSchema):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class DoctorsSpecializationsResponseSchema(BaseModel):
    data: Optional[list[DoctorSpecializationReadSchema]]
    total: int
    limit: int
    offset: int
