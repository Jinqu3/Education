

from src.database import async_session_maker
from src.schemas.bookings import Booking
from src.repository.base import BaseRepository
from src.models.bookings import BookingsORM

class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking