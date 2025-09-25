from sqlalchemy import select

from database import async_session_maker
from schemas.hotels import Hotel
from src.repository.base import BaseRepository
from src.models.hotels import HotelsORM

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    async def get_all(
            self,
            location: str,
            title: str,
            limit: int,
            offset: int,
    ):

        query = select(self.model)
        if location:
            query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
        if title:
            query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel,from_attributes=True) for hotel in result.scalars().all()]