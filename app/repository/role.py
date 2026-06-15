from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from app.db.models.role import Role


class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name(self, name: str) -> Role | None:
        stmt = select(Role).where(Role.name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Role | None:
        stmt = select(Role).where(Role.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Role:
        role = Role(name=name)
        self.session.add(role)
        await self.session.flush()
        return role

    async def get_all(self, offset: int = 0, limit: int = 100) -> List[Role]:
        stmt = select(Role).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        values = result.scalars().all()
        return list(values)

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(Role)
        result = await self.session.execute(stmt)
        return result.scalar_one()
