from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.vendor.models.vendor import VendorModel
from application.vendor.schemas.vendor import VendorCreate, VendorView, VendorUpdate, VendorCreateRequest
from uuid import UUID
from fastapi import HTTPException

class Vendor(BaseService[VendorModel, VendorCreate, VendorView, VendorUpdate]):
    def __init__(self, session: AsyncSession):
        model = VendorModel(session)
        super().__init__(model, VendorView)

    async def create(self, user_id: str, payload: VendorCreateRequest) -> VendorView:
        vendor_dict = payload.model_dump()
        vendor_dict["user_id"] = UUID(user_id)
        vendor_data = VendorCreate(**vendor_dict)
        result = await self.model.create(vendor_data)
        return self.read_schema.model_validate(result, from_attributes=True)
    
    async def update(self, user_id: str, payload: VendorCreateRequest) -> VendorView:
        result = await self.model.update(user_id, payload)
        if result:
            return self.read_schema.model_validate(result, from_attributes=True)
        if not result:
            raise HTTPException(status_code=404, detail="Resource with given id not found")