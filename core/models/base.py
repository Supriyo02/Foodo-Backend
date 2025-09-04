from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar, Generic, Type, Optional
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

TModel = TypeVar("TModel", bound="Base")

class Base(Generic[TModel]):
    def __init__(self, session: AsyncSession, model: Type[TModel]):
        self.db = session
        self.model = model

    async def create(self, payload):
        data = self.model(**payload.model_dump())
        self.db.add(data)
        try:
            await self.db.commit()
            await self.db.refresh(data)
            return data
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def list(self, limit: int = 10, offset: int = 0) -> List[TModel]:
        try:
            result = await self.db.execute(select(self.model).limit(limit).offset(offset))
            return result.scalars().all()
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def view(self, id: str) -> Optional[TModel]:
        try:
            result = await self.db.execute(select(self.model).where(self.model.id == id))
            return result.scalars().first()
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def update(self, id: str, payload) -> Optional[TModel]:
        try:
            q = select(self.model).where(self.model.id == id)
            result = await self.db.execute(q)
            obj = result.scalars().first()
            if not obj:
                return None
            update_data = payload.model_dump()
            for field, value in update_data.items():
                setattr(obj, field, value)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
                   
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete(self, id: str) -> None:
        try:
            result = await self.db.execute(delete(self.model).where(self.model.id == id))
            await self.db.commit()
            return result.rowcount > 0
        except SQLAlchemyError:
            await self.db.rollback()
            raise
