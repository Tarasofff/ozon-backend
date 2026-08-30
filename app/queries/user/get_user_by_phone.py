from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import User


async def get_user_by_phone(db: AsyncSession, phone: str) -> User | None:
    stmt = select(User).where(User.phone == phone)
    return await db.scalar(stmt)
