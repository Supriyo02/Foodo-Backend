# models/auth.py
import uuid
from sqlalchemy import Column, String, DateTime, func, Enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from db.base import Base
from core.models.base import Base as BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

class User(Base):
    __tablename__ = "users"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(10), nullable=False)
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
    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def create(self, payload: dict):
        data = self.model(**payload)
        self.db.add(data)
        try:
            await self.db.commit()
            await self.db.refresh(data)
            return data
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_user_by_email(self, email: str) -> Optional[User]:
        try:
            q = select(self.model).where(self.model.email == email)
            res = await self.db.execute(q)
            user = res.scalars().first()
            return user
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def get_user_by_id(self, id: str) -> Optional[User]:
        try:
            q = select(User).where(User.id == id)
            res = await self.db.execute(q)
            user = res.scalars().first()
            return user
        except SQLAlchemyError:
            self.db.rollback()
            raise



