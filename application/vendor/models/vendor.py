import uuid
from sqlalchemy import Column, String, Boolean, DECIMAL, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.base import Base as BaseModel

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(pgUUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kitchen_name = Column(String(150), nullable=False)
    kitchen_description = Column(String, nullable=True)
    kitchen_image_url = Column(String(255), nullable=True)
    address = Column(String, nullable=False)
    latitude = Column(DECIMAL(9, 6), nullable=False)
    longitude = Column(DECIMAL(9, 6), nullable=False)
    is_verified = Column(Boolean, server_default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

class VendorModel(BaseModel[Vendor]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Vendor)
