from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from fastapi import Response

from src.services.auth import AuthService
from src.schemas.users import UserRequestADD,UserAdd
from src.api.dependencies import UserIdDep,DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])



@router.post("/register")
async def register_user(
        data: UserRequestADD,
        db: DBDep
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email,hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
    except IntegrityError:
        raise HTTPException(500,detail="user already exists")
    await db.commit()
    return {"status": "OK"}

@router.post("/login")
async def login_user(
        data: UserRequestADD,
        response: Response,
        db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user or not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(401, detail="Invalid credentials")

    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie(
        "access_token",
        access_token
    )

    return {"access_token": access_token}

@router.get("/me")
async def get_me(
        user_id: UserIdDep,
        db: DBDep
):
    return await db.users.get_one_or_none(id=user_id)

@router.post("/logout")
async def logout_user(
    response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK"}



