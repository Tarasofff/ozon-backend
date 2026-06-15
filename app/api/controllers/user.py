from fastapi import APIRouter, Depends, Query, status
from app.api.dependencies import check_login_user, check_register_user, check_token
from app.config.config import app_config
from app.db.models import User
from app.db.session import get_session
from app.repository.role import RoleRepository
from app.schemas.role import PaginatedUserRolesResponse
from app.schemas.user import UserAuthResponse, UserCreate
from app.services.jwt import JWTService
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix=app_config.api_v1_prefix.user, tags=["Users"])


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    jwt_service = JWTService()
    return UserService(jwt_service=jwt_service, session=session)


def get_user_role_repository(
    session: AsyncSession = Depends(get_session),
) -> RoleRepository:
    return RoleRepository(session=session)


@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreate = Depends(check_register_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.create(user)


@router.post("/login", response_model=UserAuthResponse, status_code=status.HTTP_200_OK)
async def login(
    user: User = Depends(check_login_user),
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.login(user)


@router.get(
    "/role",
    response_model=PaginatedUserRolesResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(check_token)],
)
async def get_all_user_roles(
    limit: int = Query(100, ge=1, le=100),  # по умолчанию 10, от 1 до 100
    offset: int = Query(0, ge=0),  # по умолчанию 0, не может быть отрицательным
    role_repository: RoleRepository = Depends(get_user_role_repository),
):
    roles = await role_repository.get_all(offset=offset, limit=limit)

    # Исключаем администратора, TODO query
    roles = [role for role in roles if role.name != app_config.user_role.ADMIN]
    count = len(roles)  # обновляем total после фильтрации

    return PaginatedUserRolesResponse.model_validate(
        {
            "data": roles,
            "total": count,
            "limit": limit,
            "offset": offset,
        }
    )
