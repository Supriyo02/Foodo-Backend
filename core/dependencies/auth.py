# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..config.config import settings
from jose import jwt, JWTError
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login") 

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

        sub_raw = payload.get("sub")
        if sub_raw is None:
            raise credentials_exception

        sub = json.loads(sub_raw)
        if "user_id" not in sub:
            raise credentials_exception

        return sub
    except JWTError:
        raise credentials_exception
