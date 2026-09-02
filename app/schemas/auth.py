from datetime import datetime
from typing import TypedDict
from app.schemas import DoctorRead, NurseRead, UserRead
from app.schemas.shared.base_schema import BaseSchema
from app.schemas.shared.types import PasswordStr, PhoneStr


class AccessTokenPayload(TypedDict):
    user_id: int
    user_role: str


class EncodedAccessTokenPayload(AccessTokenPayload):
    exp: datetime
    iat: datetime


class AccessToken(BaseSchema):
    access_token: str
    token_type: str


class AuthPayload(BaseSchema):
    phone: PhoneStr
    password: PasswordStr


class AuthResponse(BaseSchema):
    user: UserRead
    profile: DoctorRead | NurseRead
    token: AccessToken
