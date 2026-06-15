from app.config.config import app_config
from app.repository.role import RoleRepository
from app.schemas.user import UserCreateSchema
from app.services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.utils import to_date


class UserAdminSeeder:
    def __init__(
        self,
        user_service: UserService,
        role_repo: RoleRepository,
        session: AsyncSession,
    ):
        self.user_service = user_service
        self.role_repo = role_repo
        self.session = session

    async def seed(self):
        async with self.session.begin():
            existing_admin = await self.user_service.get_by_phone(
                app_config.user_admin_config.phone
            )

            if existing_admin:
                return

            # role = await self.role_repo.get_by_name(app_config.user_role.ADMIN)
            role = await self.role_repo.get_by_name(app_config.user_role.NURSE)
            # role = await self.role_repo.get_by_name(app_config.user_role.DOCTOR)

            if not role:
                raise ValueError("Role not found")

            # user_data = UserCreateSchema(
            #     first_name=app_config.user_admin_config.first_name,
            #     middle_name=app_config.user_admin_config.middle_name,
            #     last_name=app_config.user_admin_config.last_name,
            #     phone=app_config.user_admin_config.phone,
            #     email=app_config.user_admin_config.email,
            #     date_of_birth=to_date(app_config.user_admin_config.date_of_birth),
            #     password=app_config.user_admin_config.password,
            #     role_id=admin_role.id,
            #     is_active=True,
            # )

            user_data = UserCreateSchema(
                first_name="Olga",
                middle_name="Solovyova",
                last_name="Petrova",
                phone="0731413179",
                email="email@gmail.com",
                date_of_birth=to_date(app_config.user_admin_config.date_of_birth),
                password=app_config.user_admin_config.password,
                role_id=role.id,
                is_active=True,
            )

            return await self.user_service.create(user_data)
