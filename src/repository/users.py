from src.repository.mappers.mappers import UserDataMapper
from src.repository.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import UserWithHashedPassword

from sqlalchemy import select
from pydantic import EmailStr, BaseModel


class UsersRepository(BaseRepository):
    model = UsersORM
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr) -> BaseModel:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return UserWithHashedPassword.model_validate(res, from_attributes=True)
