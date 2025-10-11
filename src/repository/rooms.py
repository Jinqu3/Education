from src.repository.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room
from src.database import engine

from sqlalchemy import select,func
from datetime import date

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id,date_from,date_to)

        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))
