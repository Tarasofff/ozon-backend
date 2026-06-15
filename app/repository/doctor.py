from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.models import Doctor, User
from sqlalchemy.orm import selectinload


class DoctorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_doctor_by_user_id(self, user_id: int) -> Doctor | None:
        stmt = select(Doctor).where(Doctor.user_id == user_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, offset: int = 0, limit: int = 100) -> list[Doctor]:
        stmt = (
            select(Doctor)
            .offset(offset)
            .limit(limit)
            .join(Doctor.user)
            .where(User.is_active)
            .options(
                selectinload(Doctor.user).load_only(
                    User.id,
                    User.first_name,
                    User.middle_name,
                    User.last_name,
                    User.phone,
                    User.email,
                    User.date_of_birth,
                )
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_count(self) -> int:
        stmt = select(func.count()).select_from(Doctor).join(Doctor.user).where(User.is_active)
        result = await self.session.execute(stmt)
        return result.scalar_one()
