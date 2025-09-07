from __future__ import annotations
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.orm import relationship
from .association import categories_items
import uuid
from db.base import Base
from sqlalchemy.ext.associationproxy import association_proxy
from typing import TYPE_CHECKING
from core.models.base import Base as BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

if TYPE_CHECKING:
    from .category import Category

class Category(Base):
    __tablename__ = "categories"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    items = relationship("Item", secondary=categories_items, back_populates="categories")

    meals_categories = relationship("MealCategory", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)
    meals = association_proxy("meals_categories", "meal")

class CategoryModel(BaseModel[Category]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Category)