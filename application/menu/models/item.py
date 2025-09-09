from __future__ import annotations
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Column, String, ForeignKey, Boolean, DECIMAL, DateTime, func, select
from core.models.base import Base as BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
import uuid
from db.base import Base
from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from .category import Category
from ..schemas.item import MapCategoryItem

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
        secondary="categories_items",
        back_populates="items",
        cascade="all, delete",
        lazy="selectin"
    )

class ItemModel(BaseModel[Item]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Item)

    async def map_item_to_category(self, item_id: str, category_id: str) -> MapCategoryItem:
        item = await self.db.get(Item, item_id)
        category = await self.db.get(Category, category_id)

        if not item or not category:
            raise ValueError("Item or Category not found")
        if category not in item.categories:
            item.categories.append(category)

        try:
            await self.db.commit()
            await self.db.refresh(item)
            return MapCategoryItem(category_id=category.id, item_id=item.id)
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def unmap_category_item(self, item_id: str, category_id: str) -> MapCategoryItem:
        item = await self.db.get(Item, item_id)
        category = await self.db.get(Category, category_id)

        if not item or not category:
            raise ValueError("Item or Category not found")

        if category not in item.categories:
            raise ValueError("Item doesn't belong to the category")
        
        item.categories.remove(category)

        try:
            await self.db.commit()
            return MapCategoryItem(category_id=category.id, item_id=item.id)
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_items_by_category(self, category_id: str, limit:int, offset: int) -> list[Item]:
        stmt = (
            select(Item)
            .join(Item.categories)
            .where(Item.categories.any(id=category_id))
            .limit(limit).offset(offset)
        )
        try:
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError:
            self.db.rollback()
            raise
