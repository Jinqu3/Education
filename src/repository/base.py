from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from fastapi import HTTPException


class BaseRepository():
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self,*args,**kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self,model_data: BaseModel):
        stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def update(self,model_data:BaseModel, **filter_by) -> None:


        if not await self.get_one_or_none(**filter_by):
            raise HTTPException(status_code=404, detail="Объект не найден")

        if count(await self.get_all(**filter_by)) > 1:
        raise HTTPException(status_code=422, detail="Объектов больше чем 1")

        stmt = update(self.model).filter_by(**filter_by).values(**model_data.model_dump())
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        if count(await self.get_all(**filter_by)) > 1:
            raise HTTPException(status_code=422, detail="Объектов больше чем 1")

        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)