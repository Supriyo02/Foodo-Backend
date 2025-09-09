from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

class MealCategory(BaseModel):
    meal_id: uuid.UUID
    category_id: uuid.UUID
    position: Optional[int] = None

    model_config = {"from_attributes": True}

class MealCategoryCreate(MealCategory):
    pass

class MealCategoryUpdate(MealCategory):
    pass

class MealCategoryView(MealCategory):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]