from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .services.auth import Auth as AuthService
from .schemas.user import UserCreate
from .schemas.refresh_token import TokenResponse
from db.session import get_session

router = APIRouter()

async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserCreate,
    request: Request = None,
    service: AuthService = Depends(get_auth_service),
):
    return await service.authenticate(payload.name, payload.password_hash, user_agent=request.headers.get("user-agent"), ip=request.client.host if request.client else None)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    payload: dict,
    request: Request = None,
    service: AuthService = Depends(get_auth_service),
):
    return await service.rotate_refresh_token(payload, user_agent=request.headers.get("user-agent"), ip=request.client.host if request.client else None)

@router.post("/revoke", response_model=dict)
async def revoke(payload: dict, service: AuthService = Depends(get_auth_service)):
    return await service.revoke_refresh_token(payload)
