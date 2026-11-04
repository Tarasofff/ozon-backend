from fastapi import APIRouter, Depends, status
from app.core.config import routes
from app.database.session import get_db_session
from app.schemas import AuthResponse, AuthPayload
from app.schemas.user import UserRead
from app.services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.user_mapper import user_to_read

auth_router = APIRouter(prefix=routes.auth, tags=["Auth"])


def get_auth_service(db: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(session=db)


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=AuthResponse)
async def login(
    auth_payload: AuthPayload,
    auth_service: AuthService = Depends(get_auth_service),
):
    user, access_token = await auth_service.login(auth_payload=auth_payload)

    return AuthResponse(
        user=UserRead.model_validate(user),
        profile=user_to_read(user),
        token=access_token,
    )
