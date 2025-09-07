from __future__ import annotations
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Column, String, ForeignKey, Boolean, DECIMAL, DateTime, func
from core.models.base import Base as BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from .association import categories_items
import uuid
from db.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from ...vendor.models.vendor import Vendor
    from .category import Category

class Item(Base):
    __tablename__ = "items"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    vendor_id = Column(PG_UUID(as_uuid=True), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(150), nullable=False, index=True)
    description = Column(String, nullable=True)
    image_url = Column(String(255), nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    is_available = Column(Boolean, server_default=expression.true(), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vendor = relationship("Vendor", back_populates="items", passive_deletes=True)
    categories = relationship(
        "Category",
        secondary=categories_items,
        back_populates="items",
        cascade="all, delete",
    )

class ItemModel(BaseModel[Item]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Item)