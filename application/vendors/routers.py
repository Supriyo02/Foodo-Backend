from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from .services.vendors import Vendor as VendorService
from .schemas.vendors import VendorCreate, VendorUpdate, VendorView
from typing import List

router = APIRouter()

async def get_vendor_service(session: AsyncSession = Depends(get_session)) -> VendorService:
    return VendorService(session)

@router.post("/create", response_model=VendorView, status_code=201)
async def create(payload: VendorCreate, service: VendorService = Depends(get_vendor_service)):
    return await service.create(payload)

@router.get("/list", response_model=List[VendorView])
async def list(service: VendorService = Depends(get_vendor_service)):
    return await service.list()