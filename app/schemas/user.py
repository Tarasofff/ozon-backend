from pydantic import EmailStr
from datetime import date
from app.database.models.enums.user_role import UserRole
from app.schemas import NurseCreate, DoctorCreate
from app.schemas.shared import BaseSchema
from app.schemas.shared.types import (
    FirstNameStr,
    LastNameStr,
    PatronymicStr,
    PhoneStr,
    PasswordStr,
)
from .shared import BaseCreate, BaseRead


class UserBase(BaseSchema):
    first_name: FirstNameStr
    patronymic: PatronymicStr
    last_name: LastNameStr
    phone: PhoneStr
    email: EmailStr | None = None
    date_of_birth: date
    is_active: bool = True
    role: UserRole


class UserAccount(BaseCreate, UserBase):
    password: PasswordStr


class UserCreate(BaseCreate):
    user: UserAccount
    profile: DoctorCreate | NurseCreate


class UserRead(BaseRead, UserBase):
    pass
