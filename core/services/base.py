# core/base_service.py
from typing import TypeVar, Generic, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TRead = TypeVar("TRead")

class Base(Generic[TModel, TCreate, TRead]):
    def __init__(self, session: AsyncSession, model: Type[TModel], read_schema: Type[TRead]):
        self.session = session
        self.model = model
        self.read_schema = read_schema

    async def list(self) -> List[TRead]:
        results = await TModel.list(self.session)
        return [TModel.model_validate(result, from_attribute=True) for result in results]

    async def create(self, payload: TCreate) -> TRead:
        result = await TModel.create(self.session, payload)
        return TRead.model_validate(result, from_attributes=True)
