from datetime import date
from sqlalchemy import select

from src.repository.mappers.mappers import BookingDataMapper
from src.database import async_session_maker
from src.schemas.bookings import Booking
from src.repository.base import BaseRepository
from src.models.bookings import BookingsORM

class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingDataMapper

    async def get_bookings_with_today_check_in(self):
        query = (
            select(self.model)
            .filter(self.model.date_from==date.today())
        )
        bookings = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(booking) for booking in bookings.scalars().all()]