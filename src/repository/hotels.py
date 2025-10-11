from sqlalchemy import select
from datetime import date

from database import async_session_maker
from models.rooms import RoomsORM
from schemas.hotels import Hotel
from src.repository.base import BaseRepository
from src.models.hotels import HotelsORM

class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel

    # async def get_all(
    #     self,
    #     location: str,
    #     title: str,
    #     limit: int,
    #     offset: int,
    # ) -> list[Hotel]:
    #     query = select(self.model)
    #     if location:
    #         query = query.filter(HotelsORM.location.ilike(f"%{location}%"))
    #     if title:
    #         query = query.filter(HotelsORM.title.ilike(f"%{title}%"))
    #     query = (
    #         query
    #         .limit(limit)
    #         .offset(offset)
    #     )
    #     result = await self.session.execute(query)
    #     return [Hotel.model_validate(hotel,from_attributes=True) for hotel in result.scalars().all()]

    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            offset: int,
            limit: int,
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_idx_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.hotel_id.in_(rooms_ids_to_get))
        )
        query = await self.get_filtered(HotelsORM.id.in_(hotels_idx_to_get))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        return query