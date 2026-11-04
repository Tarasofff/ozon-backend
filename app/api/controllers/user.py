from fastapi import APIRouter, status, Depends
from app.core.config import routes
from app.schemas.auth import AuthPayload, AuthResponse
from app.schemas.user import UserCreate, UserRead
from app.services.auth import AuthService
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session
from app.utils.user_mapper import user_to_read

user_router = APIRouter(prefix=routes.user, tags=["User"])


def get_auth_service(db: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(session=db)


def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(db)


@user_router.post(
    "/create", status_code=status.HTTP_201_CREATED, response_model=AuthResponse
)
async def create(
    register_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
):
    user = await user_service.create(register_data)

    authenticated_user, access_token = await auth_service.login(
        auth_payload=AuthPayload(phone=user.phone, password=register_data.user.password)
    )

    return AuthResponse(
        user=UserRead.model_validate(authenticated_user),
        profile=user_to_read(authenticated_user),
        token=access_token,
    )
