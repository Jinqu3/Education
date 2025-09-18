from src.repository.base import BaseRepository
from src.models.users import UsersORM
from src.schemas.users import User, UserWithHashedPassword,UserRequestADD
from sqlalchemy import select
from pydantic import EmailStr, ValidationError


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_user_with_hashed_password(self, email:EmailStr)->str:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one()
        return UserWithHashedPassword.model_validate(res, from_attributes=True)