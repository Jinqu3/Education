from fastapi import APIRouter, HTTPException
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repository.users import UsersRepository
from src.schemas.users import UserRequestADD,UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(
        data: UserRequestADD,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email,hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except IntegrityError:
            return HTTPException(500,detail="user already exists")
        await session.commit()
    return {"status": OK}
