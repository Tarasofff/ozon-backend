from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import date
from .shared import BaseCreate, BaseRead
from .token import Token


class UserBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    phone: str
    email: Optional[EmailStr]
    date_of_birth: date
    is_active: bool
    role_id: int


# class UserCreateSchema(PasswordHashMixin, DateParser, UserBase):
#     model_config = ConfigDict(strict=True)


class UserCreate(BaseCreate, UserBase):
    password: str


class UserRead(BaseRead, UserBase):
    pass


class UserAuth(BaseModel):
    phone: str
    password: str


class UserAuthResponse(UserRead, Token):
    pass
