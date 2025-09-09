# core/base_service.py
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy import select
from ..models.base import Base as BaseModel
from fastapi import HTTPException

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TView = TypeVar("TView")
TUpdate = TypeVar("TUpdate")

class Base(Generic[TModel, TCreate, TView, TUpdate]):
    def __init__(self, model: BaseModel[TModel], read_schema: Type[TView]):
        self.model = model
        self.read_schema = read_schema

    async def create(self, payload: TCreate) -> TView:
        result = await self.model.create(payload)
        return self.read_schema.model_validate(result, from_attributes=True)
    
    async def list(self, limit: int, offset: int) -> List[TView]:
        results = await self.model.list(limit, offset)
        return [self.read_schema.model_validate(r, from_attributes=True) for r in results]

    async def view(self, id: str) -> Optional[TView]:
        result = await self.model.view(id)
        if result:
            return self.read_schema.model_validate(result, from_attributes=True)
        if not result:
            raise HTTPException(status_code=404, detail="Resource with given id not found")
    
    async def update(self, id: str, payload: TUpdate) -> Optional[TView]:
        result = await self.model.update(id, payload)
        if result:
            return self.read_schema.model_validate(result, from_attributes=True)
        if not result:
            raise HTTPException(status_code=404, detail="Resource with given id not found")
    
    async def delete(self, id: str) -> bool:
        result = await self.model.delete(id)
        if result:
            return result
        if not result:
            raise HTTPException(status_code=404, detail="Resource with given id not found")
