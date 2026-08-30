from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import AsyncSessionLocal


async def get_db(
    auto_commit: bool = False,
) -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            if auto_commit:
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
