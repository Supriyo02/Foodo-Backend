from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.vendor.models.vendor import VendorModel
from application.vendor.schemas.vendor import VendorCreate, VendorView, VendorUpdate

class Vendor(BaseService[VendorModel, VendorCreate, VendorView, VendorUpdate]):
    def __init__(self, session: AsyncSession):
        model = VendorModel(session)
        super().__init__(model, VendorView)