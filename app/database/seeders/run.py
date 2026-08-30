import asyncio
from app.database.session import AsyncSessionLocal


# sequence matters!!!
async def async_main():
    async with AsyncSessionLocal() as session:

        print("[DB] Seeders complete")


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
