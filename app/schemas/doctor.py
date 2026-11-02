from app.schemas.shared import BaseCreate, BaseRead
from app.schemas.shared.base_schema import BaseSchema


class DoctorBase(BaseSchema):
    pass


class DoctorCreate(BaseCreate, DoctorBase):
    pass


class DoctorRead(BaseRead, DoctorBase):
    pass
