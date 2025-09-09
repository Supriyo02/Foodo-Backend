from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.menu.models.meal import MealModel
from application.vendor.models.vendor import VendorModel
from application.menu.schemas.meal import MealCreate, MealUpdate, MealView, MealCreateRequest
from uuid import UUID
from fastapi import HTTPException

class Meal(BaseService[MealModel, MealCreate, MealView, MealUpdate]):
    def __init__(self, session: AsyncSession):
        model = MealModel(session)
        self.vendor_model = VendorModel(session)
        super().__init__(model, MealView)

    async def create(self, user_id: str, payload: MealCreateRequest) -> MealView:
        vendor = await self.vendor_model.get_vendor_by_user_id(user_id)
        if vendor is None:
            raise HTTPException(status_code=404, detail="Vendor details with your user id not found.")
        vendor_id = vendor.id
        meal_dict = payload.model_dump()
        meal_dict["vendor_id"] = vendor_id
        meal_data = MealCreate(**meal_dict)
        result = await self.model.create(meal_data)
        return self.read_schema.model_validate(result, from_attributes=True)