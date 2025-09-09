from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.menu.models.item import ItemModel
from application.vendor.models.vendor import VendorModel
from application.menu.schemas.item import ItemCreate, ItemUpdate, ItemView, ItemCreateRequest, MapCategoryItem
from uuid import UUID
from fastapi import HTTPException

class Item(BaseService[ItemModel, ItemCreate, ItemView, ItemUpdate]):
    def __init__(self, session: AsyncSession):
        model = ItemModel(session)
        self.vendor_model = VendorModel(session)
        super().__init__(model, ItemView)

    async def create(self, user_id: str, payload: ItemCreateRequest) -> ItemView:
        vendor = await self.vendor_model.get_vendor_by_user_id(user_id)
        if vendor is None:
            raise HTTPException(status_code=404, detail="Vendor details with your user id not found.")
        vendor_id = vendor.id
        item_dict = payload.model_dump()
        item_dict["vendor_id"] = vendor_id
        item_data = ItemCreate(**item_dict)
        result = await self.model.create(item_data)
        return self.read_schema.model_validate(result, from_attributes=True)
    
    async def update(self, user_id: str, id:str, payload: ItemCreateRequest) -> ItemView:
        vendor = await self.vendor_model.get_vendor_by_user_id(user_id)
        if vendor is None:
            raise HTTPException(status_code=404, detail="Vendor details with your user id not found.")
        vendor_id = vendor.id
        item_dict = payload.model_dump()
        item_dict["vendor_id"] = vendor_id
        item_data = ItemCreate(**item_dict)
        result = await self.model.update(id, item_data)
        if result:
            return self.read_schema.model_validate(result, from_attributes=True)
        if not result:
            raise HTTPException(status_code=404, detail="Item with given id not found")
        
    async def map_category_item(self, payload: MapCategoryItem) -> MapCategoryItem:
        item_id = payload.item_id
        category_id = payload.category_id
        try:
            return await self.model.map_item_to_category(item_id, category_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def unmap_category_item(self, payload: MapCategoryItem) -> MapCategoryItem:
        item_id = payload.item_id
        category_id = payload.category_id
        try:
            return await self.model.unmap_category_item(item_id, category_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def get_items_by_category(self, category_id: str, limit:int, offset:int) -> list[ItemView]:
        results = await self.model.get_items_by_category(category_id, limit, offset)
        return [self.read_schema.model_validate(r, from_attributes=True) for r in results]
