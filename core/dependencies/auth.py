# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..config.config import settings
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from application.user.models.user import User
from sqlalchemy import select
from db.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  
async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM]
        )

        sub = payload.get("sub")
        if not sub or "user_id" not in sub:
            raise credentials_exception

        user_id = sub["user_id"]
        role = sub.get("role")
        name = sub.get("name")

        return {"user_id": user_id, "role": role, "name": name}
    except JWTError:
        raise credentials_exception
