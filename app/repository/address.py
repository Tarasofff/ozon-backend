from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Address


class AddressRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_address(
        self,
        country_name: str,
        city_name: str,
        street_name: str,
        building_number: str,
    ) -> Address | None:
        stmt = select(Address).where(
            Address.country_name == country_name,
            Address.city_name == city_name,
            Address.street_name == street_name,
            Address.building_number == building_number,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(
        self,
        country_name: str,
        city_name: str,
        street_name: str,
        building_number: str,
        postal_code: str,
    ) -> Address:
        value = Address(
            country_name=country_name,
            city_name=city_name,
            street_name=street_name,
            building_number=building_number,
            postal_code=postal_code,
        )
        self.session.add(value)
        await self.session.flush()
        return value
