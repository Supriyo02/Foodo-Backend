from sqlalchemy.ext.asyncio import AsyncSession
from ..models.item import Item as ItemModel

class Menu():
    def __init__(self, session: AsyncSession):
        model = ItemModel(session)