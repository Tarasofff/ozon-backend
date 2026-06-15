from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class DiagnoseBaseSchema(BaseModel):
    name: str


class DiagnoseCreateSchema(DiagnoseBaseSchema):
    pass


class DiagnoseReadSchema(DiagnoseBaseSchema):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class DiagnosesResponseSchema(BaseModel):
    data: Optional[list[DiagnoseReadSchema]]
    total: int
    limit: int
    offset: int
