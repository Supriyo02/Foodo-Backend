from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from .services.vendor import Vendor as VendorService
from .schemas.vendor import VendorCreate, VendorUpdate, VendorView
from typing import List, Optional
from pydantic import UUID4

router = APIRouter()

async def get_vendor_service(session: AsyncSession = Depends(get_session)) -> VendorService:
    return VendorService(session)

@router.post("/create", response_model=VendorView, status_code=201)
async def create(payload: VendorCreate, service: VendorService = Depends(get_vendor_service)):
    return await service.create(payload)

@router.get("/list", response_model=List[VendorView])
async def list(limit: Optional[int] = 10, offset: Optional[int] = 0, service: VendorService = Depends(get_vendor_service)):
    return await service.list(limit= limit, offset= offset)

@router.get("/view/{id}", response_model=VendorView)
async def view(id: UUID4, service: VendorService = Depends(get_vendor_service)):
    return await service.view(id)

@router.put("/update/{id}", response_model=VendorView)
async def update(id: UUID4, payload: VendorUpdate, service: VendorService = Depends(get_vendor_service)):
    return await service.update(id, payload)

@router.delete("/delete/{id}", status_code=204)
async def delete(id: UUID4, service: VendorService = Depends(get_vendor_service)):
    await service.delete(id)
    return Response(status_code=204)