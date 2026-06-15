from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import Post


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_number_and_cabinet_id(
        self, number: str, cabinet_id: int
    ) -> Post | None:
        stmt = select(Post).where(
            Post.number == number,
            Post.cabinet_id == cabinet_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, number: str, cabinet_id: int) -> Post:
        value = Post(number=number, cabinet_id=cabinet_id)
        self.session.add(value)
        await self.session.flush()
        return value
