from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
from datetime import datetime
class User(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = "customer"

    model_config = {"from_attributes": True}

class UserCreate(User):
    password_hash: str

class UserView(User):
    id: uuid.UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]