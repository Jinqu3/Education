from sqlalchemy import select, func
from datetime import date

from src.repository.mappers.mappers import HotelDataMapper
from src.models.rooms import RoomsORM
from src.schemas.hotels import Hotel
from src.repository.base import BaseRepository
from src.models.hotels import HotelsORM
from src.repository.utils import rooms_ids_for_booking
from src.exceptions import DatesCannotBeEqualException,InvalidDateOrderException


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel
    mapper = HotelDataMapper

    async def get_filtered_by_time(
        self,
        date_from: date,
        date_to: date,
        location,
        title,
        limit,
        offset,
    ) -> list[Hotel]:
        if date_from > date_to:
            raise InvalidDateOrderException
        if date_from == date_to:
            raise DatesCannotBeEqualException

        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomsORM.hotel_id)
            .select_from(RoomsORM)
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )

        query = select(HotelsORM).filter(HotelsORM.id.in_(hotels_ids_to_get))
        if location:
            query = query.filter(func.lower(HotelsORM.location).contains(location.strip().lower()))
        if title:
            query = query.filter(func.lower(HotelsORM.title).contains(title.strip().lower()))
        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(hotel) for hotel in result.scalars().all()]
