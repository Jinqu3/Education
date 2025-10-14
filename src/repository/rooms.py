from src.models.facilities import RoomsFacilitiesORM
from src.repository.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room
from src.database import engine
from src.repository.utils import rooms_ids_for_booking

from sqlalchemy import select,func,delete
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

        rooms_ids_to_get = rooms_ids_for_booking(hotel_id=hotel_id,date_from=date_from,date_to=date_to)

        return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))

    async def get_facilities_ids(self, **filter_by):
        query = (
            select(RoomsFacilitiesORM.facility_id)
            .join(self.model, self.model.id == RoomsFacilitiesORM.room_id)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        facility_ids = [row[0] for row in result.all()]
        return facility_ids

    async def delete_room_facilities(self, room_id:int, facilities_ids: list[int]) -> None:
        stmt = delete(RoomsFacilitiesORM).where(
            RoomsFacilitiesORM.room_id == room_id,
            RoomsFacilitiesORM.facility_id.in_(facilities_ids)
        )
        await self.session.execute(stmt)
        await self.session.commit()