from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User
from app.database.models.doctor import Doctor
from app.database.models.enums.user_role import UserRole
from app.database.models.nurse import Nurse
from app.infrastructure.security.hash import hash_password
from app.repository import UserRepository
from app.schemas.user import UserCreate

ROLE_TO_MODEL_MAP: dict[UserRole, type[User]] = {
    UserRole.DOCTOR: Doctor,
    UserRole.NURSE: Nurse,
}


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repo = UserRepository(session=session)

    def _build_user(self, register_data: UserCreate) -> User:
        user_data = register_data.user.model_dump(
            exclude={"password"},
        )
        user_data["password_hash"] = hash_password(
            register_data.user.password,
        )

        model_cls = ROLE_TO_MODEL_MAP[register_data.user.role]

        return model_cls(
            **user_data,
            **register_data.profile.model_dump(),
        )

    async def create(self, register_data: UserCreate) -> User:
        user = self._build_user(register_data)

        self.user_repo.add(user)

        await self.session.flush()

        return user
