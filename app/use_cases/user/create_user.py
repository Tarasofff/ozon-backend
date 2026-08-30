from typing import Type
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import EntityAlreadyExistsException
from app.database.models import User
from app.database.models.doctor import Doctor
from app.database.models.enums.user_role import UserRole
from app.database.models.nurse import Nurse
from app.infrastructure.bcrypt import hash_password
from app.queries.user import get_user_by_phone
from app.schemas.user_unions import UserCreateUnion, UserReadUnion

ROLE_TO_MODEL_MAP: dict[UserRole, type[User]] = {
    UserRole.DOCTOR: Doctor,
    UserRole.NURSE: Nurse,
}


class CreateUserUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(
        self, dto: UserCreateUnion, response_schema: Type[UserReadUnion]
    ) -> UserReadUnion:
        # 1. Проверка уникальности
        existing_user = await get_user_by_phone(self.db, dto.phone)
        if existing_user:
            raise EntityAlreadyExistsException()

        # 2. Подготовка данных
        user_data = dto.model_dump(exclude={"password"})
        user_data["password_hash"] = hash_password(dto.password)

        # 3. Выбор конкретного ORM-класса
        model_cls = ROLE_TO_MODEL_MAP.get(dto.role, User)

        # 4. Инстанцирование дочерней модели
        user = model_cls(**user_data)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        # 5. Валидация через переданную схему
        return response_schema.model_validate(user)
