from pydantic import BaseModel
from fastapi import Depends,Query,Request,HTTPException
from typing import Annotated

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default = 1, ge=1,title="Page")]
    per_page: Annotated[int | None, Query(default = 5, ge=1,le=20,title="PerPage")]

PaginationDep = Annotated[PaginationParams,Depends()]

def get_token(request: Request) -> str:
    access_token = request.cookies.get("access_token", None)
    if not access_token:
        raise HTTPException(status_code=401, detail="Token not found")
    return access_token

def get_current_user_id(access_token: str =  Depends(get_token)) -> int:
    data = AuthService().decode_token(access_token)
    return data["user_id"]

UserIdDep = Annotated[int,Depends(get_current_user_id)]

