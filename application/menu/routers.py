from core.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from .schemas.item import ItemView, ItemCreateRequest, MapCategoryItem
from .schemas.meal import MealView, MealCreateRequest
from .schemas.category import CategoryView, CategoryCreateRequest
from .schemas.mealcategory import MealCategoryCreate, MealCategoryUpdate, MealCategoryView
from .services.meal import Meal as MealService
from .services.item import Item as ItemService
from .services.category import Category as CategoryService
from .services.mealcategory import MealCategory as MealCategoryService
from typing import Optional, List

router = APIRouter()

async def get_item_service(session: AsyncSession = Depends(get_session)) -> ItemService:
    return ItemService(session)

async def get_category_service(session: AsyncSession = Depends(get_session)) -> CategoryService:
    return CategoryService(session)

async def get_meal_service(session: AsyncSession = Depends(get_session)) -> MealService:
    return MealService(session)

async def get_mealcategory_service(session: AsyncSession = Depends(get_session)) -> MealCategoryService:
    return MealCategoryService(session)

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

@router.get("/item/list", response_model=List[ItemView])
async def item_list(
    limit: Optional[int] = 10, offset: Optional[int] = 0,
    service: ItemService = Depends(get_item_service)
):
    return await service.list(limit=limit, offset=offset)

@router.post("/category/create", response_model=CategoryView)
async def category_create(
    payload: CategoryCreateRequest,
    service: CategoryService = Depends(get_category_service),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    return await service.create(user_id, payload)

@router.get("/category/list", response_model=List[CategoryView])
async def category_list(
    limit: Optional[int] = 10, offset: Optional[int] = 0,
    service: CategoryService = Depends(get_category_service)
):
    return await service.list(limit=limit, offset=offset)

@router.post("/category/add-item", response_model=MapCategoryItem)
async def map_category_item(
    payload: MapCategoryItem,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    return await service.map_category_item(payload)

@router.post("/category/remove-item", response_model=MapCategoryItem)
async def unmap_category_item(
    payload: MapCategoryItem,
    service: ItemService = Depends(get_item_service),
    current_user: dict = Depends(get_current_user)
):
    return await service.unmap_category_item(payload)

@router.get("/category/{category_id}/view-items", response_model=List[ItemView])
async def get_items_by_category(
    category_id: str,
    limit: Optional[int] = 10, offset: Optional[int] = 0,
    service: ItemService = Depends(get_item_service)
):
    return await service.get_items_by_category(category_id, limit, offset)

@router.post("/meal/create", response_model=MealView)
async def meal_create(
    payload: MealCreateRequest,
    service: MealService = Depends(get_meal_service),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["user_id"]
    return await service.create(user_id, payload)

@router.get("/meal/view/{id}", response_model=dict)
async def meal_view(
    id: str,
    service: MealCategoryService = Depends(get_mealcategory_service)
):
    return await service.view_meal(id)

@router.get("/meal/list", response_model=List[MealView])
async def meal_list(
    limit: Optional[int] = 10, offset: Optional[int] = 0,
    service: MealService = Depends(get_meal_service)
):
    return await service.list(limit=limit, offset=offset)

@router.post("/meal/add-category", response_model=MealCategoryView)
async def mealcategory_create(
    payload: MealCategoryCreate,
    service: MealCategoryService = Depends(get_mealcategory_service),
    current_user: dict = Depends(get_current_user)
):
    return await service.create(payload)

@router.post("/meal/remove-category", response_model=MealCategoryView)
async def mealcategory_delete(
    payload: MealCategoryCreate,
    service: MealCategoryService = Depends(get_mealcategory_service),
    current_user: dict = Depends(get_current_user)
):
    return await service.delete(payload)