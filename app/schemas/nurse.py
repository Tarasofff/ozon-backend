from app.schemas.shared.base_schema import BaseSchema
from app.schemas.shared import BaseCreate, BaseRead


class NurseBase(BaseSchema):
    pass


class NurseCreate(BaseCreate, NurseBase):
    pass


class NurseRead(BaseRead, NurseBase):
    pass
