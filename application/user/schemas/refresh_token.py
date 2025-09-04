from pydantic import BaseModel, EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str  # client must store securely (prefer httpOnly cookie)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str