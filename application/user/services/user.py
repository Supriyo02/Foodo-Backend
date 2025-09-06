from core.services.base import Base as BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from application.user.models.user import UserModel
from application.user.schemas.user import UserCreate, UserView, UserUpdate
from core.security.auth import hash_password

class User(BaseService[UserModel, UserCreate, UserView, UserUpdate]):
    def __init__(self, session: AsyncSession):
        model = UserModel(session)
        super().__init__(model, UserView)

    async def register(self, payload: UserCreate) -> UserView:
        user_data = payload.model_dump()
        user_data["password_hash"] = hash_password(user_data.pop("password"))
        result = await self.model.create(user_data)
        return self.read_schema.model_validate(result, from_attributes=True)