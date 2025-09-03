from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, TypeVar
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T", bound="Base")

class Base:
    @classmethod
    async def create(cls, db: AsyncSession, payload):
        data = cls(**payload.dict())
        db.add(data)
        try:
            await db.commit()
            await db.refresh(data)
            return data
        except SQLAlchemyError:
            await db.rollback()
            raise

    @classmethod
    async def list(cls, db: AsyncSession, limit: int = 10, offset: int = 0) -> List[T]:
        try:
            result = await db.execute(select(cls).limit(limit).offset(offset))
            return result.scalars().all()
        except SQLAlchemyError:
            await db.rollback()
            raise