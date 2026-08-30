from typing import Literal
from app.database.models.enums.user_role import UserRole
from app.schemas.user import UserBase, UserCreate, UserRead


class NurseBase(UserBase):
    role: Literal[UserRole.NURSE] = UserRole.NURSE


class NurseCreate(UserCreate, NurseBase):
    pass


class NurseRead(UserRead, NurseBase):
    pass
