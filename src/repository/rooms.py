from src.repository.base import BaseRepository
from src.models.rooms import RoomsORM

class HotelRepository(BaseRepository):
    model = RoomsORM