import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, func, select
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from db.base import Base
from core.models.base import Base as BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from core.config.config import settings
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(PG_UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False)
    user_agent = Column(String(255), nullable=True)
    ip_address = Column(String(100), nullable=True)
    revoked = Column(Boolean, server_default="false", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="refresh_tokens")

class RefreshTokenModel(BaseModel[RefreshToken]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, RefreshToken)

    async def create(self, *, token_hash: str, user_id: uuid.UUID, expires_delta: timedelta | None = None, user_agent: str | None = None, ip: str | None = None) -> RefreshToken:
        expires_at = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        db_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            user_agent=user_agent,
            ip_address=ip,
            expires_at=expires_at,
            revoked=False
        )
        self.db.add(db_token)
        try:
            await self.db.commit()
            await self.db.refresh(db_token)
            return db_token
        except SQLAlchemyError:
            await self.db.rollback()
            raise

    async def get_token_by_token_hash(self, token_hash: str) -> Optional[RefreshToken]:
        try:
            q = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
            res = await self.db.execute(q)
            db_token = res.scalars().first()
            if not db_token or db_token.revoked or db_token.expires_at < datetime.now(timezone.utc):
                return None
            db_token.revoked = True
            self.db.add(db_token)
            await self.db.commit()
            return db_token
        except SQLAlchemyError:
            self.db.rollback()
            raise

    async def revoke_refresh_token(self, token_hash: str) -> bool:
        q = select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        res = await self.db.execute(q)
        db_token = res.scalars().first()
        if not db_token:
            return False
        db_token.revoked = True
        try:
            self.db.add(db_token)
            await self.db.commit()
            return True
        except SQLAlchemyError:
            await self.db.rollback()
            raise
