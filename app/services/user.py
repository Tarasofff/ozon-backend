from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.database.models.doctor import Doctor
from app.database.models.enums.user_role import UserRole
from app.database.models.nurse import Nurse
from app.infrastructure.hash import hash_password
from app.repository import UserRepository
from app.schemas.user_unions import UserCreateUnion

ROLE_TO_MODEL_MAP: dict[UserRole, type[User]] = {
    UserRole.DOCTOR: Doctor,
    UserRole.NURSE: Nurse,
}


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session=session)

    async def create(self, dto: UserCreateUnion) -> User:
        user_data = dto.model_dump(exclude={"password"})
        user_data["password_hash"] = hash_password(dto.password)

        model_cls = ROLE_TO_MODEL_MAP.get(dto.role, User)

        user = model_cls(**user_data)

        self.user_repo.add(user)

        await self.session.flush()

        return user
