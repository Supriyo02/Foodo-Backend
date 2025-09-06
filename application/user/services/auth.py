# services/auth_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User, UserModel
from ..models.refresh_token import RefreshToken, RefreshTokenModel
from core.security.auth import (
    verify_password, create_access_token,
    generate_refresh_token_raw, hash_refresh_token
)
from datetime import timedelta
from typing import Tuple
import uuid
from fastapi import HTTPException, status
from ..schemas.refresh_token import TokenResponse

class Auth:
    def __init__(self, session: AsyncSession):
        self.user_model = UserModel(session)
        self.refresh_token_model = RefreshTokenModel(session)

    async def authenticate(self, email: str, password: str, user_agent: str | None, ip: str | None = None) -> TokenResponse:
        user = await self.user_model.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
        access_token = create_access_token(user_id=str(user.id), name=user.name, role=user.role)
        raw_refresh, db_token = await self.create_refresh_token(user_id=user.id, user_agent=user_agent, ip=ip)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": raw_refresh}

    async def create_refresh_token(self, user_id: uuid.UUID, *, expires_delta: timedelta | None = None, user_agent: str | None = None, ip: str | None = None) -> Tuple[str, RefreshToken]:
        raw = generate_refresh_token_raw()
        token_hash = hash_refresh_token(raw)
        db_token = await self.refresh_token_model.create(token_hash=token_hash, user_id=user_id, expires_delta=expires_delta, user_agent=user_agent, ip=ip)
        return raw, db_token
    
    async def rotate_refresh_token(self, payload: dict, user_agent: str | None = None, ip: str | None = None) -> TokenResponse:
        raw_refresh = payload.get("refresh_token")
        if not raw_refresh:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="refresh_token required")
        hashed = hash_refresh_token(raw_refresh)
        db_token = await self.refresh_token_model.get_token_by_token_hash(token_hash=hashed)
        if not db_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        raw_new, new_db_token = await self.create_refresh_token(db_token.user_id, user_agent=user_agent, ip=ip)
        user = await self.user_model.get_user_by_id(new_db_token.user_id)
        access_token = create_access_token(user_id=str(user.id), name=user.name, role=user.role)
        return {"access_token": access_token, "token_type": "bearer", "refresh_token": raw_new}

    async def revoke_refresh_token(self, payload: dict) -> bool:
        raw_refresh = payload.get("refresh_token")
        if not raw_refresh:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="refresh_token required")
        hashed = hash_refresh_token(raw_refresh)
        ok = await self.refresh_token_model.revoke_refresh_token(token_hash=hashed)
        if not ok:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
        return {"ok": ok}
