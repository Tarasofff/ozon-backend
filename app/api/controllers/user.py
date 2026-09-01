from fastapi import APIRouter, status, Depends
from app.core.config import routes
from app.database.models.enums.user_role import UserRole
from app.database.session import get_db_session
from app.schemas.doctor import DoctorRead
from app.schemas.nurse import NurseRead
from app.schemas.user_unions import UserCreateUnion, UserReadUnion
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.user import UserService

user_router = APIRouter(prefix=routes.user, tags=["User"])


def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(db)


@user_router.post(
    "/create",
    response_model=UserReadUnion,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    dto: UserCreateUnion,
    user_service: UserService = Depends(get_user_service),
):
    schema_map = {
        UserRole.DOCTOR: DoctorRead,
        UserRole.NURSE: NurseRead,
    }
    response_schema = schema_map[dto.role]

    user = await user_service.create(dto)

    return response_schema.model_validate(user)
