from fastapi import APIRouter, status, Depends
from app.core.config import routes
from app.database.models.enums.user_role import UserRole
from app.schemas.user import UserCreate
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db_session

user_router = APIRouter(prefix=routes.user, tags=["User"])


def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(db)


@user_router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
)
async def create(
    register_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    await user_service.create(register_data)


@user_router.get("/roles", status_code=status.HTTP_200_OK, response_model=list[str])
async def get_user_roles():
    return [role.value for role in UserRole]
