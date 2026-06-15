from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.role import RoleRepository
from app.config.config import app_config


class RoleSeeder:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.role_repo = RoleRepository(session)

    async def seed(self):
        async with self.session.begin():
            existing_roles = {role.name for role in await self.role_repo.get_all()}

            for role_name in app_config.user_role.list():
                if role_name not in existing_roles:
                    await self.role_repo.create(role_name)
