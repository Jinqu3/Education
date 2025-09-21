from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import Response

from src.services.auth import AuthService
from src.database import async_session_maker
from src.repository.users import UsersRepository
from src.schemas.users import UserRequestADD,UserAdd
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



@router.post("/register")
async def register_user(
        data: UserRequestADD,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email,hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except IntegrityError:
            return HTTPException(500,detail="user already exists")
        await session.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(
        data: UserRequestADD,
        response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(404, detail="Password doesn't match")
        if not user:
            raise HTTPException(401,detail="User not found")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.get("/me")
async def get_me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        return await UsersRepository(session).get_one_or_none(id=user_id)

@router.post("/logout")
async def logout_user(
    response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK"}



