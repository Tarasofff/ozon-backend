from app.db.models import User
from app.repository import UserRepository
from app.schemas.user import (
    UserPartialSchema,
    UserCreateSchema,
    UserLoginSchema,
    UserReadSchema,
)
from app.services import JWTService
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:

    def __init__(
        self,
        jwt_service: JWTService,
        session: AsyncSession,
    ):
        self.user_repo = UserRepository(session=session)
        self.jwt_service = jwt_service
        self.session = session

    def get_token(self, user: User):
        payload = self.jwt_service.get_payload(user)
        return self.jwt_service.encode(payload)

    async def create(self, user_data: UserCreateSchema):
        user = User(**user_data.model_dump())

        created_user = await self.user_repo.create(user)

        created_user_dump = UserReadSchema.model_validate(created_user).model_dump()

        token_data = self.get_token(created_user)

        await self.session.commit()

        return UserLoginSchema.model_validate(
            {**token_data.model_dump(), **created_user_dump}
        )

    async def login(self, user: User):
        token_data = self.get_token(user)
        user_data = UserReadSchema.model_validate(user).model_dump()

        return UserLoginSchema(**token_data.model_dump(), **user_data)

    async def get_by_phone(self, phone: str):
        return await self.user_repo.get_by_phone(phone)

    async def update(self, id: int, user_data: UserPartialSchema):
        fields_to_update = user_data.model_dump(exclude_none=True)
        return await self.user_repo.update(id, fields_to_update)
