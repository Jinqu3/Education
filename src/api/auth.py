from fastapi import APIRouter, HTTPException, Response

from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, UserAlreadyExistsHTTPException,IncorrectPasswordHTTPException, IncorrectPasswordException, \
    UserNotFoundException, UserNotFoundHTTPException
from src.services.auth import AuthService
from src.schemas.users import UserRequestADD, UserAdd
from src.api.dependencies import UserIdDep, DBDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestADD,
    db: DBDep
):
    try:
        await AuthService(db).register_user(
            data=data,
        )
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException(email=data.email)
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestADD, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data=data)
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def get_me(
    user_id: UserIdDep,
    db: DBDep
):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
