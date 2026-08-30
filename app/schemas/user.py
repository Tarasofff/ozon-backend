from pydantic import EmailStr, Field
from datetime import date
from app.schemas.shared import BaseSchema
from app.schemas.shared.types import (
    FirstNameStr,
    LastNameStr,
    PatronymicStr,
    PhoneStr,
    PasswordStr,
)
from .shared import BaseCreate, BaseRead


class UserToken(BaseSchema):
    access_token: str = Field(min_length=10, max_length=255)
    token_type: str = Field(min_length=3, max_length=20)


class UserBase(BaseSchema):
    first_name: FirstNameStr
    patronymic: PatronymicStr
    last_name: LastNameStr
    phone: PhoneStr
    email: EmailStr | None = None
    date_of_birth: date
    is_active: bool = True
    hospital_id: int


class UserCreate(BaseCreate, UserBase):
    password: PasswordStr


class UserRead(BaseRead, UserBase):
    pass


class UserAuth(BaseSchema):
    phone: PhoneStr
    password: PasswordStr


class UserAuthResponse(BaseSchema):
    user: UserRead
    token: UserToken
