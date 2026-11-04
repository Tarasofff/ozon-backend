import asyncio
from app.database.seeders.seeds.hospital_data_seed import HospitalDataSeeder
from app.database.session import AsyncSessionLocal


async def async_main():
    async with AsyncSessionLocal() as session:

        await HospitalDataSeeder(session).seed()

        print("[DB] Seeders complete")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
