from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.menu.models.category import CategoryModel
from application.vendor.models.vendor import VendorModel
from application.menu.schemas.category import CategoryCreate, CategoryView, CategoryUpdate, CategoryCreateRequest
from fastapi import HTTPException

class Category(BaseService[CategoryModel, CategoryCreate, CategoryView, CategoryUpdate]):
    def __init__(self, session: AsyncSession):
        model = CategoryModel(session)
        self.vendor_model = VendorModel(session)
        super().__init__(model, CategoryView)

    async def create(self, user_id: str, payload: CategoryCreateRequest) -> CategoryView:
        vendor = await self.vendor_model.get_vendor_by_user_id(user_id)
        if vendor is None:
            raise HTTPException(status_code=404, detail="Vendor details with your user id not found.")
        vendor_id = vendor.id
        item_dict = payload.model_dump()
        item_dict["vendor_id"] = vendor_id
        item_data = CategoryCreate(**item_dict)
        result = await self.model.create(item_data)
        return self.read_schema.model_validate(result, from_attributes=True)