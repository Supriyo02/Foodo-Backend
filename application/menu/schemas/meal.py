from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

class Meal(BaseModel):
    vendor_id: uuid.UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_price: float
    is_available: bool = True

    model_config = {"from_attributes": True}

class MealCreate(Meal):
    pass

class MealCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    base_price: float
    is_available: bool = True

    model_config = {"from_attributes": True}

class MealUpdate(Meal):
    pass


class MealView(Meal):
    id: uuid.UUID
    created_at: datetime
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]