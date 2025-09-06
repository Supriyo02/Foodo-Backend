from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from .services.vendor import Vendor as VendorService
from .schemas.vendor import VendorCreate, VendorUpdate, VendorView, VendorCreateRequest
from typing import List, Optional
from pydantic import UUID4
from uuid import UUID
from core.dependencies.auth import get_current_user

router = APIRouter()

async def get_vendor_service(session: AsyncSession = Depends(get_session)) -> VendorService:
    return VendorService(session)

@router.post("/create", response_model=VendorView, status_code=201)
async def create(payload: VendorCreateRequest, service: VendorService = Depends(get_vendor_service), current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return await service.create(user_id, payload)

@router.get("/list", response_model=List[VendorView])
async def list(limit: Optional[int] = 10, offset: Optional[int] = 0, service: VendorService = Depends(get_vendor_service)):
    return await service.list(limit= limit, offset= offset)

@router.get("/view/{id}", response_model=VendorView)
async def view(id: UUID4, service: VendorService = Depends(get_vendor_service)):
    return await service.view(id)

@router.put("/update", response_model=VendorView)
async def update(payload: VendorCreateRequest, service: VendorService = Depends(get_vendor_service), current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    return await service.update(user_id, payload)

@router.delete("/delete/{id}", status_code=204)
async def delete(id: UUID4, service: VendorService = Depends(get_vendor_service)):
    await service.delete(id)
    return Response(status_code=204)