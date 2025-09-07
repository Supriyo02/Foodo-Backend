from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.menu.models.category import CategoryModel
from application.menu.schemas.category import CategoryCreate, CategoryView, CategoryUpdate

class Category(BaseService[CategoryModel, CategoryCreate, CategoryView, CategoryUpdate]):
    def __init__(self, session: AsyncSession):
        model = CategoryModel(session)
        super().__init__(model, CategoryView)