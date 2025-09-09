from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.menu.models.association import MealCategoryModel
from application.menu.schemas.mealcategory import MealCategoryCreate, MealCategoryUpdate, MealCategoryView
from fastapi import HTTPException

class MealCategory(BaseService[MealCategoryModel, MealCategoryCreate, MealCategoryView, MealCategoryUpdate]):
    def __init__(self, session: AsyncSession):
        model = MealCategoryModel(session)
        super().__init__(model, MealCategoryView)

    async def create(self, payload: MealCategoryCreate) -> MealCategoryView:
        try:
            result = await self.model.create(meal_id=payload.meal_id, category_id=payload.category_id, position=payload.position)
            return self.read_schema.model_validate(result, from_attributes=True)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
    async def delete(self, payload: MealCategoryCreate) -> MealCategoryView:
        result = await self.model.delete(meal_id=payload.meal_id, category_id=payload.category_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Resource with found")
        return self.read_schema.model_validate(result, from_attributes=True)
    
    async def view_meal(self, meal_id: str) -> dict:
        result = await self.model.view_meal(meal_id)
        if result is None:
            raise HTTPException(status_code=404, detail="Resource with found")
        return result