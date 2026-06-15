from fastapi import Depends
from app.api.exceptions.api_exceptions import (
    UnprocessableEntityException,
)
from app.db.session import get_session
from app.schemas.user import UserCreateSchema
from app.services.jwt import JWTService
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    jwt_service = JWTService()
    return UserService(jwt_service=jwt_service, session=session)


async def check_register_user(
    user_data: UserCreateSchema, user_service: UserService = Depends(get_user_service)
):
    user_validate = UserCreateSchema.model_validate(user_data)

    result = await user_service.get_by_phone(user_validate.phone)
    if result:
        raise UnprocessableEntityException("User already exists")

    return user_validate
