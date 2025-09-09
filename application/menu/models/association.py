from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table, func, Index, select
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from db.base import Base
import uuid
from sqlalchemy.orm import relationship, joinedload
from core.models.base import Base as BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from .meal import Meal
from .category import Category
from sqlalchemy.exc import SQLAlchemyError

categories_items = Table(
    "categories_items",
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

class MealCategoryModel(BaseModel[MealCategory]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MealCategory)


    async def create(self, meal_id: str, category_id: str, position: int | None = None) -> MealCategory:

        meal = await self.db.get(Meal, meal_id)
        category = await self.db.get(Category, category_id)

        if not meal or not category:
            raise ValueError("Meal or Category not found")

        mapping = MealCategory(
            meal_id=meal_id,
            category_id=category_id,
            position=position,
        )

        self.db.add(mapping)

        try:
            await self.db.commit()
            await self.db.refresh(mapping)
            return mapping
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def delete(self, meal_id: str, category_id: str) -> MealCategory | None:
        mapping = (
            await self.db.execute(
                select(MealCategory)
                .where(
                    MealCategory.meal_id == meal_id,
                    MealCategory.category_id == category_id,
                )
                .limit(1)
            )
        ).scalars().first()

        if not mapping:
            return None

        await self.db.delete(mapping)

        try:
            await self.db.commit()
            return mapping
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def view_meal(self, meal_id: str) -> dict | None:
        meal = (
            await self.db.execute(
                select(Meal)
                .where(Meal.id == meal_id)
                .options(joinedload(Meal.meals_categories).joinedload(MealCategory.category))
            )
        ).scalars().first()

        if not meal:
            return None

        return {
            "id": str(meal.id),
            "name": meal.name,
            "description": meal.description,
            "image_url": meal.image_url,
            "base_price": str(meal.base_price) if meal.base_price else None,
            "is_available": meal.is_available,
            "categories": [
                {
                    "id": str(mc.category.id),
                    "name": mc.category.name
                }
                for mc in meal.meals_categories
            ]
        }




    