# models/auth.py
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from db.base import Base
from core.models.base import Base as BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

class User(Base):
    __tablename__ = "users"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(10), nullable=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(
        Enum("customer", "vendor", "admin", name="user_roles"),
        server_default="customer",
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

class UserModel(BaseModel[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)



