from pydantic import BaseModel
from fastapi import Depends,Query
from typing import Annotated

class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(default = 1, ge=1,title="Page")]
    per_page: Annotated[int | None, Query(default = 1, ge=1,le=20,title="PerPage")]

PaginationDep = Annotated[PaginationParams,Depends()]