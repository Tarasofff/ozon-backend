from pydantic import BaseModel
from .shared import PaginatedResponse
from .shared import BaseRead


class DoctorSpecializationBase(BaseModel):
    name: str


class DoctorSpecializationRead(BaseRead, DoctorSpecializationBase):
    pass


class PaginatedDoctorSpecializationsResponse(
    PaginatedResponse[DoctorSpecializationRead]
):
    pass
