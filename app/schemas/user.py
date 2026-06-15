from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import date
from app.schemas.mixins import PasswordHashMixin
from app.schemas.token import TokenSchema
from app.utils.utils import DateParser


class UserBaseSchema(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: Optional[EmailStr]
    date_of_birth: date
    password: str
    is_active: bool
    role_id: int


class UserCreateSchema(PasswordHashMixin, DateParser, UserBaseSchema):
    model_config = ConfigDict(strict=True)


class UserReadSchema(UserBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserAuthSchema(BaseModel):
    phone: str
    password: str


class UserLoginSchema(TokenSchema):
    id: int
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: EmailStr
    date_of_birth: date
    is_active: bool
    role_id: int


class UserPartialSchema(PasswordHashMixin, DateParser, BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    email: Optional[EmailStr]
    date_of_birth: Optional[date]
    password: Optional[str]
    role_id: Optional[int]
    is_active: Optional[bool]

    model_config = ConfigDict(strict=True)
