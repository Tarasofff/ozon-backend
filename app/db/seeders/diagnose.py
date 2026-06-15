import json
from pathlib import Path
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.config import BASE_DIR
from app.repository.diagnose import DiagnoseRepository


class DiagnoseSeeder:
    def __init__(self, session: AsyncSession, json_path: Optional[Path | str] = None):
        self.session = session
        self.diagnose_repo = DiagnoseRepository(session)
        self.json_path = Path(
            json_path or BASE_DIR / "app" / "db" / "seeders" / "data" / "diagnose.json"
        )

    async def seed(self):
        async with self.session.begin():
            with open(self.json_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for item in data:
                name = item["name"].strip()

                existing = await self.diagnose_repo.get_by_name(name)
                if existing is None:
                    await self.diagnose_repo.create(name)
