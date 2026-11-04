import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Address, Hospital, Cabinet, Post


class PostSeed(BaseModel):
    number: str


class CabinetSeed(BaseModel):
    number: str
    post: list[PostSeed]


class HospitalSeed(BaseModel):
    name: str
    number: str | None = None
    cabinet: list[CabinetSeed]


class AddressSeed(BaseModel):
    country_name: str
    city_name: str
    street_name: str
    building_number: str
    hospital: list[HospitalSeed]


class HospitalDataSeeder:
    BASE_DIR: Path = Path(__file__).resolve().parents[3]

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self.session = session
        self.json_path = Path(
            self.BASE_DIR / "database/seeders/data/address_hospital.json"
        )

    async def seed(self) -> None:
        with self.json_path.open("r", encoding="utf-8") as file:
            raw_data: list[dict[str, Any]] = json.load(file)

        data = [AddressSeed.model_validate(item) for item in raw_data]

        if not data:
            raise ValueError("Addresses list is empty")

        async with self.session.begin():
            for address_data in data:
                await self._seed_address(address_data)

    async def _seed_address(self, data: AddressSeed) -> None:
        stmt = select(Address).where(
            Address.country_name == data.country_name,
            Address.city_name == data.city_name,
            Address.street_name == data.street_name,
            Address.building_number == data.building_number,
        )

        address = await self.session.scalar(stmt)

        if address is None:
            address = Address(
                country_name=data.country_name,
                city_name=data.city_name,
                street_name=data.street_name,
                building_number=data.building_number,
            )
            self.session.add(address)
            await self.session.flush()

        for hospital_data in data.hospital:
            await self._seed_hospital(hospital_data, address.id)

    async def _seed_hospital(
        self,
        data: HospitalSeed,
        address_id: int,
    ) -> None:
        stmt = select(Hospital).where(
            Hospital.name == data.name,
            Hospital.address_id == address_id,
            Hospital.number == data.number,
        )

        hospital = await self.session.scalar(stmt)

        if hospital is None:
            hospital = Hospital(
                name=data.name,
                address_id=address_id,
                number=data.number,
            )
            self.session.add(hospital)
            await self.session.flush()

        for cabinet_data in data.cabinet:
            await self._seed_cabinet(cabinet_data, hospital.id)

    async def _seed_cabinet(
        self,
        data: CabinetSeed,
        hospital_id: int,
    ) -> None:
        stmt = select(Cabinet).where(
            Cabinet.number == data.number,
            Cabinet.hospital_id == hospital_id,
        )

        cabinet = await self.session.scalar(stmt)

        if cabinet is None:
            cabinet = Cabinet(
                number=data.number,
                hospital_id=hospital_id,
            )
            self.session.add(cabinet)
            await self.session.flush()

        for post_data in data.post:
            await self._seed_post(post_data, cabinet.id)

    async def _seed_post(
        self,
        data: PostSeed,
        cabinet_id: int,
    ) -> None:
        stmt = select(Post).where(
            Post.number == data.number,
            Post.cabinet_id == cabinet_id,
        )

        post = await self.session.scalar(stmt)

        if post is None:
            self.session.add(
                Post(
                    number=data.number,
                    cabinet_id=cabinet_id,
                )
            )
