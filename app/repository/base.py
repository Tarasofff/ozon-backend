from typing import Generic, Sequence, Type, TypeVar
from sqlalchemy import ColumnElement, func, select, exists
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: int) -> ModelType | None:
        return await self.session.get(self.model, id)

    async def get_one_or_none(
        self,
        *whereclause: ColumnElement[bool],
    ) -> ModelType | None:
        stmt = select(self.model).filter(*whereclause)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *whereclause: ColumnElement[bool],
        order_by: Sequence[ColumnElement[object]] = (),
        limit: int | None = 100,
        offset: int | None = 0,
    ) -> Sequence[ModelType]:

        stmt = select(self.model).filter(*whereclause)

        if order_by:
            stmt = stmt.order_by(*order_by)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count(self, *whereclause: ColumnElement[bool]) -> int:
        stmt = select(func.count()).select_from(self.model).filter(*whereclause)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def exists(self, *whereclause: ColumnElement[bool]) -> bool:
        stmt = select(exists().where(*whereclause))
        result = await self.session.execute(stmt)
        return result.scalar_one()

    def add(self, entity: ModelType) -> ModelType:
        self.session.add(entity)
        return entity
