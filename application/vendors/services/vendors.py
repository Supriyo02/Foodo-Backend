from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.vendors.models.vendors import Vendor
from application.vendors.schemas.vendors import VendorCreate, VendorView

class Vendor(BaseService[Vendor, VendorCreate, VendorView]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Vendor, VendorView)