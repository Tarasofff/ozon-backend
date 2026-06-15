import asyncio
from app.db.seeders.diagnose import DiagnoseSeeder
from app.db.seeders.address_hospital import AddressHospitalSeeder
from app.db.seeders.role import RoleSeeder
from app.db.session import AsyncSessionLocal
from app.db.seeders.user_admin import UserAdminSeeder
from app.repository.role import RoleRepository
from app.services.jwt import JWTService
from app.services.user import UserService
from app.db.seeders.specialization import SpecializationSeeder


# sequence matters!!!
async def main():
    async with AsyncSessionLocal() as session:

        # Role seed
        role_seeder = RoleSeeder(session)
        await role_seeder.seed()

        # Admin seed
        role_repo = RoleRepository(session)
        jwt_service = JWTService()
        user_service = UserService(jwt_service, session)

        user_admin_seeder = UserAdminSeeder(
            user_service=user_service,
            role_repo=role_repo,
            session=session,
        )

        # await user_admin_seeder.seed() #TODO

        # address hospital seed
        locations_seeder = AddressHospitalSeeder(session)
        await locations_seeder.seed()

        # Diagnose seeder
        diagnose_seeder = DiagnoseSeeder(session)
        await diagnose_seeder.seed()

        # Specialization seeder
        specialization_seeder = SpecializationSeeder(session)
        await specialization_seeder.seed()

        print("All seeders complete")


if __name__ == "__main__":
    asyncio.run(main())
