from sqlalchemy.exc import NoResultFound
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from src.repository.mappers.base import DataMapper

from src.exceptions import *

class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.mapper.map_to_domain_entity(res)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            res = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(res)

    async def add(self, model_data: BaseModel):
        stmt = insert(self.model).values(**model_data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        try:
            res = result.scalars().one()
        except:
            raise CanNotAddObjectException
        return self.mapper.map_to_domain_entity(res)

    async def add_bulk(self, model_data: Sequence[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in model_data])
        await self.session.execute(add_data_stmt)

    async def update(self, model_data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        """
        param: exclude_unset bool - True when we use patch method and False when use put method
        """
        if not await self.get_one_or_none(**filter_by):
            raise ObjectNotFoundException

        stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**model_data.model_dump(exclude_unset=exclude_unset))
        )
        try:
            await self.session.execute(stmt)
        except:
            raise CanNotСhangeObjectException

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model).filter_by(**filter_by)
        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except:
            raise CanNotDeleteObjectException