from pydantic import BaseModel
from .shared import BaseRead, PaginatedResponse


class DiagnoseBase(BaseModel):
    name: str


class DiagnoseCreate(DiagnoseBase):
    pass


class DiagnoseRead(BaseRead, DiagnoseBase):
    pass


class PaginatedDiagnosesResponse(PaginatedResponse[DiagnoseRead]):
    pass
