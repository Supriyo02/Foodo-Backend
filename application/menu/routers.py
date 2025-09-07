from core.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from .schemas.item import ItemView, ItemCreateRequest
from .schemas.category import CategoryCreate, CategoryView
from .services.category import Category as CategoryModel
from .services.item import Item as ItemService
from .services.category import Category as CategoryService
from typing import Optional, List

router = APIRouter()

async def get_item_service(session: AsyncSession = Depends(get_session)) -> ItemService:
    return ItemService(session)

async def get_category_service(session: AsyncSession = Depends(get_session)) -> CategoryService:
    return CategoryService(session)

@router.post("/item/create", response_model=ItemView)
async def item_create(
    payload: ItemCreateRequest,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    return await service.create(user_id, payload)

@router.put("/item/update/{id}", response_model=ItemView)
async def item_update(
    id: str,
    payload: ItemCreateRequest,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    return await service.update(user_id, id, payload)

@router.get("/item/view/{id}", response_model=ItemView)
async def item_view(
    id: str,
    service: ItemService = Depends(get_item_service)
):
    return await service.view(id)

@router.post("/category/create", response_model=CategoryView)
async def category_create(
    payload: CategoryCreate,
    service: CategoryService = Depends(get_category_service)
):
    return await service.create(payload)

@router.get("/category/list", response_model=List[CategoryView])
async def category_list(
    limit: Optional[int] = 10, offset: Optional[int] = 0,
    service: CategoryService = Depends(get_category_service)
):
    return await service.list(limit=limit, offset=offset)