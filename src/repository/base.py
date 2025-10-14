from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from fastapi import HTTPException


class BaseRepository():
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session


    async def get_filtered(self,*filter,**filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(row,from_attributes=True) for row in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        else:
            return self.schema.model_validate(res,from_attributes=True)

    async def add(self,model_data: BaseModel):
        stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        else:
            return self.schema.model_validate(res, from_attributes=True)

    async def add_bulk(self,model_data: BaseModel):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in model_data])
        await self.session.execute(add_data_stmt)


    async def update(self,model_data:BaseModel, exclude_unset:bool = False, **filter_by) -> None:
        """
        param: exclude_unset bool - True when we use patch method and False when use put method
        """
        if not await self.get_one_or_none(**filter_by):
            raise HTTPException(status_code=404, detail="Объект не найден")

        stmt = (update(self.model)
                .filter_by(**filter_by)
                .values(**model_data.model_dump(exclude_unset=exclude_unset))
                )
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(stmt)
        await self.session.commit()