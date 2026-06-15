from typing import Optional
from pydantic import BaseModel
from app.schemas.user import UserRead
from .shared import BaseRead, PaginatedResponse


class DoctorBase(BaseModel):
    specialization_id: int
    user_id: int


class DoctorReadSchema(BaseRead, DoctorBase):
    user: Optional[UserRead]


class PaginatedDoctorsResponse(PaginatedResponse[DoctorReadSchema]):
    pass
