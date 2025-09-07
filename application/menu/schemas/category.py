from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime

class Category(BaseModel):
    name: str

    model_config = {"from_attributes": True}

class CategoryCreate(Category):
    pass

class CategoryUpdate(Category):
    pass

class CategoryView(Category):
    id: uuid.UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]