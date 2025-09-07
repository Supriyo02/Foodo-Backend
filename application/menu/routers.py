from core.dependencies.auth import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_session
from .schemas.item import ItemView, ItemCreateRequest
from .services.item import Item as ItemService

router = APIRouter()

async def get_item_service(session: AsyncSession = Depends(get_session)) -> ItemService:
    return ItemService(session)

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