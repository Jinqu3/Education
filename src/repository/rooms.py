from src.repository.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import RoomWithRels
from src.repository.utils import rooms_ids_for_booking
from src.repository.mappers.mappers import RoomDataMapper

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import date

class RoomsRepository(BaseRepository):
    model = RoomsORM
    mapper = RoomDataMapper

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        print(rooms_ids_to_get)

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsORM.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRels.model_validate(model) for model in result.unique().scalars().all()]

    async def get_one_or_none_with_rels(
            self,
            **filter_by
    ):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        model = result.unique().scalars().one_or_none()
        if model is None:
            return None
        return RoomWithRels.model_validate(model)

