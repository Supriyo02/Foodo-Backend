from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from .services.auth import Auth as AuthService
from .services.user import User as UserService
from .schemas.user import UserCreate, UserLogin, UserView
from .schemas.refresh_token import TokenResponse
from db.session import get_session
from pydantic import UUID4

router = APIRouter()

async def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)

async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)

@router.post("/register", response_model=UserView)
async def register(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    return await service.register(payload)

@router.get("/view/{id}", response_model=UserView)
async def view(
    id: UUID4,
    service: UserService = Depends(get_user_service),
):
    return await service.view(id)

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: UserLogin,
    request: Request = None,
    service: AuthService = Depends(get_auth_service),
):
    return await service.authenticate(payload.email, payload.password_hash, user_agent=request.headers.get("user-agent"), ip=request.client.host if request.client else None)

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
