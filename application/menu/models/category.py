from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from db.base import Base
from sqlalchemy.ext.associationproxy import association_proxy
from core.models.base import Base as BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class Category(Base):
    __tablename__ = "categories"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    vendor_id = Column(PG_UUID(as_uuid=True), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    items = relationship("Item", secondary="categories_items", back_populates="categories")
    vendor = relationship("Vendor", back_populates="categories")

    meals_categories = relationship("MealCategory", back_populates="category", cascade="all, delete-orphan", passive_deletes=True)
    meals = association_proxy("meals_categories", "meal")

class CategoryModel(BaseModel[Category]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Category)