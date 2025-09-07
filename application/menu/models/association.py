from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table, func, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from db.base import Base
import uuid
from sqlalchemy.orm import relationship

categories_items = Table(
    "category_items",
    Base.metadata,
    Column("category_id", PG_UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), primary_key=True),
    Column("item_id", PG_UUID(as_uuid=True), ForeignKey("items.id", ondelete="CASCADE"), primary_key=True),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False),
    Column("deleted_at", DateTime(timezone=True), nullable=True),
)


class MealCategory(Base):
    __tablename__ = "meals_categories"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    meal_id = Column(PG_UUID(as_uuid=True), ForeignKey("meals.id", ondelete="CASCADE"), nullable=False, index=True)
    category_id = Column(PG_UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)

    position = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    meal = relationship("Meal", back_populates="meals_categories")
    category = relationship("Category", back_populates="meals_categories")

    __table_args__ = (
        # Helpful non-unique index for lookups (allows duplicates)
        Index("ix_meals_categories_meal_id_category_id", "meal_id", "category_id"),
    )
