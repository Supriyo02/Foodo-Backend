# core/security.py
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import secrets
import hashlib
from ..config.config import settings
import json

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_ctx.verify(password, hashed_password)

def create_access_token(user_id: str, role:str, name: str, expires_delta: timedelta | None = None) -> str:
    current_time = datetime.now(timezone.utc)
    expire = current_time + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": json.dumps({"user_id": user_id, "role": role, "name": name}), "exp": int(expire.timestamp()), "iat": int(current_time.timestamp())}
    encoded = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded

# Refresh token utils
def generate_refresh_token_raw() -> str:
    # Return a high-entropy opaque token to give to the client
    return secrets.token_urlsafe(64)

def hash_refresh_token(token: str) -> str:
    # Use a fast, non-reversible hash; HMAC or bcrypt could be used. Here SHA256 for demonstration.
    # If stronger protection desired, use bcrypt/argon2 on the token.
    return hashlib.sha256(token.encode()).hexdigest()
