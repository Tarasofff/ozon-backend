from app.schemas.shared import BaseSchema, BaseCreate
from .shared import BaseRead, PaginatedResponse


class DiagnoseBase(BaseSchema):
    name: str


class DiagnoseCreate(BaseCreate, DiagnoseBase):
    pass


class DiagnoseRead(BaseRead, DiagnoseBase):
    pass


class PaginatedDiagnosesResponse(PaginatedResponse[DiagnoseRead]):
    pass
