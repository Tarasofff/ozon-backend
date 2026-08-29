import asyncio
from app.database.seeders.diagnose import DiagnoseSeeder
from app.database.seeders.address_hospital import AddressHospitalSeeder
from app.database.session import AsyncSessionLocal


# sequence matters!!!
async def async_main():
    async with AsyncSessionLocal() as session:
        # address hospital seed
        locations_seeder = AddressHospitalSeeder(session)
        await locations_seeder.seed()

        # Diagnose seeder
        diagnose_seeder = DiagnoseSeeder(session)
        await diagnose_seeder.seed()

        print("[DB] Seeders complete")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
