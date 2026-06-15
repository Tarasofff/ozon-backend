from typing import Optional
from pydantic import BaseModel, ConfigDict


class RoleReadSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AllUserRolesResponseSchema(BaseModel):
    data: Optional[list[RoleReadSchema]]
    total: int
    limit: int
    offset: int
