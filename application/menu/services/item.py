from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.menu.models.item import ItemModel
from application.vendor.models.vendor import VendorModel
from application.menu.schemas.item import ItemCreate, ItemUpdate, ItemView, ItemCreateRequest
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