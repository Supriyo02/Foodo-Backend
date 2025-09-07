from __future__ import annotations
import uuid
from sqlalchemy import Column, String, Text, Boolean, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import expression
from db.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...vendor.models.vendor import Vendor

class Meal(Base):
    __tablename__ = "meals"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    vendor_id = Column(PG_UUID(as_uuid=True), ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False, index=True)

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(255), nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, server_default=expression.true(), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    vendor = relationship("Vendor", back_populates="meals", passive_deletes=True)

    meals_categories = relationship("MealCategory", back_populates="meal", cascade="all, delete-orphan", passive_deletes=True)

    # convenience: list of Category objects via association proxy
    categories = association_proxy("meals_categories", "category")
