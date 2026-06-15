from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.models import Specialization


class SpecializationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Specialization | None:
        stmt = select(Specialization).where(Specialization.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Specialization:
        value = Specialization(name=name)
        self.session.add(value)
        await self.session.flush()
        return value

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Specialization]:
        stmt = select(Specialization).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(Specialization)
        result = await self.session.execute(stmt)
        return result.scalar_one()
