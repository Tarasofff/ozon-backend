from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Hospital


class HospitalRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_name_and_address_id(
        self, name: str, address_id: int, number: int | None = None
    ) -> Hospital | None:
        stmt = select(Hospital).where(
            Hospital.name == name,
            Hospital.address_id == address_id,
            Hospital.number == number,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Hospital | None:
        stmt = select(Hospital).where(Hospital.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self, name: str, address_id: int, number: int | None = None
    ) -> Hospital:
        value = Hospital(name=name, number=number, address_id=address_id)
        self.session.add(value)
        await self.session.flush()
        return value
