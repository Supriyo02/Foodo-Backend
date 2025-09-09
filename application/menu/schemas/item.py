from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime

class Item(BaseModel):
    vendor_id: uuid.UUID
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    is_available: bool = True

    model_config = {"from_attributes": True}

class ItemCreate(Item):
    pass

class ItemCreateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    price: float
    is_available: bool = True

    model_config = {"from_attributes": True}

class ItemUpdate(Item):
    pass

class MapCategoryItem(BaseModel):
    category_id: uuid.UUID
    item_id: uuid.UUID

class ItemView(Item):
    id: uuid.UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]