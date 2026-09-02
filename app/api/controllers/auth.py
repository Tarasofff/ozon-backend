from fastapi import APIRouter, Depends, status
from app.core.config import routes
from app.database.models.doctor import Doctor
from app.database.models.nurse import Nurse
from app.database.models.user import User
from app.database.session import get_db_session
from app.schemas import AuthResponse, AuthPayload
from app.schemas.doctor import DoctorRead
from app.schemas.nurse import NurseRead
from app.schemas.user import UserRead
from app.services.auth import AuthService
from sqlalchemy.ext.asyncio import AsyncSession

auth_router = APIRouter(prefix=routes.auth, tags=["Auth"])


def get_auth_service(db: AsyncSession = Depends(get_db_session)) -> AuthService:
    return AuthService(session=db)


def user_to_read(user: User) -> DoctorRead | NurseRead:
    if isinstance(user, Doctor):
        return DoctorRead.model_validate(user)

    if isinstance(user, Nurse):
        return NurseRead.model_validate(user)

    raise TypeError(f"Unsupported user type: {type(user).__name__}")


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
