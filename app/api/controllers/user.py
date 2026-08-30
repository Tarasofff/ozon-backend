from fastapi import APIRouter, status, Depends
from app.api.dependencies import get_db
from app.core.config import routes
from app.database.models.enums.user_role import UserRole
from app.schemas.doctor import DoctorRead
from app.schemas.nurse import NurseRead
from app.schemas.user_unions import UserCreateUnion, UserReadUnion
from sqlalchemy.ext.asyncio import AsyncSession

from app.use_cases.user.create_user import CreateUserUseCase

user_router = APIRouter(prefix=routes.user, tags=["User"])


@user_router.post(
    "/create",
    response_model=UserReadUnion,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    dto: UserCreateUnion,
    db: AsyncSession = Depends(get_db),
):
    use_case = CreateUserUseCase(db)

    schema_map = {
        UserRole.DOCTOR: DoctorRead,
        UserRole.NURSE: NurseRead,
    }
    response_schema = schema_map[dto.role]

    return await use_case.execute(dto, response_schema)
