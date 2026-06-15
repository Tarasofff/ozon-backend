from fastapi import Depends
from app.api.exceptions.api_exceptions import NotFoundException, UnauthorizedException
from app.db.models import User
from app.db.session import get_session
from app.schemas.user import UserAuthSchema
from app.services.jwt import JWTService
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.bcrypt import validate_password_str


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    jwt_service = JWTService()
    return UserService(jwt_service=jwt_service, session=session)


async def check_login_user(
    auth_data: UserAuthSchema, user_service: UserService = Depends(get_user_service)
) -> User:
    user_validate = UserAuthSchema.model_validate(auth_data)

    user = await check_user_exists(user_validate.phone, user_service)

    check_user_password(user, user_validate.password)

    return user


def check_user_password(user: User, password: str):
    compare_password = validate_password_str(password, user.password)

    if not compare_password:
        raise UnauthorizedException("User password incorrect")
    return compare_password


async def check_user_exists(phone: str, user_service: UserService) -> User:
    result = await user_service.get_by_phone(phone)
    if not result:
        raise NotFoundException("User not found")
    return result
