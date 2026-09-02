from app.database.models import User
from app.repository.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_phone(self, phone: str) -> User | None:
        return await self.get_one_or_none(
            self.model.phone == phone,
        )
