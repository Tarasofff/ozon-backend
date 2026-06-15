import json
from pathlib import Path
from typing import Optional, Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.repository import (
    HospitalRepository,
    PostRepository,
    CabinetRepository,
    AddressRepository,
)
from app.config.config import BASE_DIR


class AddressHospitalSeeder:

    def __init__(
        self, session: AsyncSession, json_path: Optional[Path | str] = None
    ) -> None:
        self.session: AsyncSession = session
        self.address_repo: AddressRepository = AddressRepository(session)
        self.hospital_repo: HospitalRepository = HospitalRepository(session)
        self.post_repo: PostRepository = PostRepository(session)
        self.cabinet_repo: CabinetRepository = CabinetRepository(session)

        self.json_path: Path = Path(
            json_path
            or BASE_DIR / "app" / "db" / "seeders" / "data" / "address_hospital.json"
        )

    async def seed(self) -> None:
        with open(self.json_path, "r", encoding="utf-8") as file:
            data: list[dict[str, Any]] = json.load(file)

        if not len(data):
            raise ValueError("Addresses list is empty")

        async with self.session.begin():
            for address_data in data:
                await self._seed_address(address_data)

    async def _seed_address(self, address_data: Dict[str, Any]) -> None:
        address = await self.address_repo.get_address(
            country_name=address_data["country_name"],
            city_name=address_data["city_name"],
            street_name=address_data["street_name"],
            building_number=address_data["building_number"],
        )

        if not address:
            address = await self.address_repo.create(
                country_name=address_data["country_name"],
                city_name=address_data["city_name"],
                street_name=address_data["street_name"],
                building_number=address_data["building_number"],
                postal_code=address_data["postal_code"],
            )

        if len(address_data["hospital"]):
            for hospital_data in address_data["hospital"]:
                await self._seed_hospital(hospital_data, address_id=address.id)

    async def _seed_hospital(
        self, hospital_data: Dict[str, Any], address_id: int
    ) -> None:
        hospital = await self.hospital_repo.get_by_name_and_address_id(
            name=hospital_data["name"],
            address_id=address_id,
            number=hospital_data.get("number"),
        )
        if not hospital:
            hospital = await self.hospital_repo.create(
                name=hospital_data["name"],
                address_id=address_id,
                number=hospital_data.get("number"),
            )

        if len(hospital_data["cabinet"]):
            for cabinet_data in hospital_data["cabinet"]:
                await self._seed_cabinet(cabinet_data, hospital.id)

    async def _seed_cabinet(
        self, cabinet_data: Dict[str, Any], hospital_id: int
    ) -> None:
        cabinet = await self.cabinet_repo.get_by_number_and_hospital_id(
            number=cabinet_data["number"], hospital_id=hospital_id
        )
        if not cabinet:
            cabinet = await self.cabinet_repo.create(
                number=cabinet_data["number"], hospital_id=hospital_id
            )

        if len(cabinet_data["post"]):
            for post_data in cabinet_data["post"]:
                await self._seed_post(post_data, cabinet.id)

    async def _seed_post(self, post_data: Dict[str, Any], cabinet_id: int) -> None:
        post = await self.post_repo.get_by_number_and_cabinet_id(
            number=post_data["number"], cabinet_id=cabinet_id
        )

        if not post:
            await self.post_repo.create(
                number=post_data["number"], cabinet_id=cabinet_id
            )
