from pydantic import BaseModel, Field, UUID4
from typing import Optional
from decimal import Decimal
from datetime import datetime

class Vendor(BaseModel):
    user_id: UUID4
    kitchen_name: str = Field(..., example="Mamma's Kitchen")
    kitchen_description: Optional[str] = Field(None, example="The best home made food in the town")
    kitchen_image_url: Optional[str] = Field(None, example="abc.aws.com")
    address: str = Field(..., example="123 Main Street, Kolkata")
    latitude: Decimal = Field(..., example=22.5726)
    longitude: Decimal = Field(..., example=88.3639)
    is_verified: Optional[bool] = Field(False, example="False")

class VendorCreate(Vendor):
    pass

class VendorCreateRequest(BaseModel):
    kitchen_name: str = Field(..., example="Mamma's Kitchen")
    kitchen_description: Optional[str] = Field(None, example="The best home made food in the town")
    kitchen_image_url: Optional[str] = Field(None, example="abc.aws.com")
    address: str = Field(..., example="123 Main Street, Kolkata")
    latitude: Decimal = Field(..., example=22.5726)
    longitude: Decimal = Field(..., example=88.3639)
    is_verified: Optional[bool] = Field(False, example="False")

class VendorUpdate(Vendor):
    user_id: None

class VendorView(Vendor):
    id: UUID4
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]