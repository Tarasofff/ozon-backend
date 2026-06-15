from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.exceptions.api_exceptions import UnauthorizedException
from app.db.session import get_session
from app.repository import RoleRepository
from app.services import JWTService
from app.config.config import app_config

bearer_scheme = HTTPBearer()


def get_jwt_service() -> JWTService:
    return JWTService()


def get_role_repo(
    session: AsyncSession = Depends(get_session),
) -> RoleRepository:
    return RoleRepository(session=session)


async def check_user_doctor_role(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
    role_repo: RoleRepository = Depends(get_role_repo),
):
    token = credentials.credentials
    decode_token = jwt_service.decode(token)
    role_id = decode_token["role_id"]

    role = await role_repo.get_by_id(role_id)

    if role and role.name != app_config.user_role.DOCTOR:
        raise UnauthorizedException("Invalid user role")

    return decode_token
