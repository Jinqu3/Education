from datetime import date
from sqlalchemy import select

from src.repository.utils import rooms_ids_for_booking
from src.schemas.bookings import BookingAdd
from src.repository.mappers.mappers import BookingDataMapper
from src.repository.base import BaseRepository
from src.models.bookings import BookingsORM
from src.exceptions import AllRoomsAreBookedException


class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_check_in(self):
        query = select(self.model).filter(self.model.date_from == date.today())
        bookings = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in bookings.scalars().all()]

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get = rooms_ids_for_booking(data.date_from, data.date_to, hotel_id)
        rooms_ids_to_book_res = await self.session.execute(rooms_ids_to_get)
        rooms_ids_to_book: list[int] = rooms_ids_to_book_res.scalars().all()

        if data.room_id in rooms_ids_to_book:
            new_booking = await self.add(data)
            return new_booking
        else:
            raise AllRoomsAreBookedException
