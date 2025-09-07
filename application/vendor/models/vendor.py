from __future__ import annotations
import uuid
from sqlalchemy import Column, String, Boolean, DECIMAL, DateTime, func, ForeignKey, select
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from db.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from core.models.base import Base as BaseModel
from sqlalchemy.orm import relationship
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...menu.models.item import Item
    from ...menu.models.meal import Meal
    from ...user.models.user import User

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
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

    user = relationship(
        "User",
        back_populates="vendor"
    )
    items = relationship("Item", back_populates="vendor")
    meals = relationship("Meal", back_populates="vendor")

class VendorModel(BaseModel[Vendor]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Vendor)

    async def update(self, id: str, payload) -> Optional[Vendor]:
        try:
            q = select(self.model).where(self.model.user_id == id)
            result = await self.db.execute(q)
            obj = result.scalars().first()
            if not obj:
                return None
            update_data = payload.model_dump()
            for field, value in update_data.items():
                setattr(obj, field, value)
            self.db.add(obj)
            await self.db.commit()
            await self.db.refresh(obj)
            return obj
                   
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_vendor_by_user_id(self, id: str) -> Optional[Vendor]:
        try:
            q = select(self.model).where(self.model.user_id == id)
            result = await self.db.execute(q)
            vendor = result.scalars().first()
            if not vendor:
                return None
            return vendor
            
        except SQLAlchemyError:
            await self.db.rollback()
            raise

