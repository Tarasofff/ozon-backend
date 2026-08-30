from pydantic import Field
from app.schemas.shared.base_schema import BaseSchema
from app.schemas.shared.types import PasswordStr, PhoneStr
from app.schemas.shared.types.identity import PhoneStr
from app.schemas.user_unions import UserReadUnion


class AccessToken(BaseSchema):
    access_token: str = Field(min_length=10, max_length=255)
    token_type: str = Field(min_length=3, max_length=20)


class AuthPayload(BaseSchema):
    phone: PhoneStr
    password: PasswordStr


class AuthResponse(BaseSchema):
    user: UserReadUnion
    token: AccessToken
