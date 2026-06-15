from pydantic import BaseModel
from .shared import BaseRead, PaginatedResponse


class RoleBase(BaseModel):
    name: str


class RoleRead(BaseRead, RoleBase):
    pass


class PaginatedUserRolesResponse(PaginatedResponse[RoleRead]):
    pass
