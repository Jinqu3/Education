from datetime import date

from src.schemas.hotels import HotelAdd,HotelPatch
from src.services.base import BaseService
from src.exceptions import check_date_to_after_date_from, ObjectNotFoundException
from src.api.dependencies import PaginationDep
from fastapi import Body
from src.exceptions import HotelNotFoundException

class HotelService(BaseService):
    async def get_filtered_by_time(self,
        pagination:PaginationDep,
        location:str | None,
        title:str | None,
        date_from: date,
        date_to: date
    ):
        check_date_to_after_date_from(date_from,date_to)
        per_page = pagination.per_page or 10
        return await self.db.hotels.get_filtered_by_time(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )

    async def get_hotel(
        self,
        hotel_id: int,
    ):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def delete_hotel(
        self,
        hotel_id: int,
    ):
       await self.db.hotels.delete(id=hotel_id)
       await self.db.commit()

    async def add_hotel(
        self,
        hotel_data: HotelAdd = Body()
    ):
        hotel =await self.db.hotels.add(hotel_data)
        return hotel

    async def change_hotel_parts(
        self,
        hotel_id: int,
        hotel_data: HotelPatch = Body(),
    ):
       await self.db.hotels.update(
            model_data=hotel_data,
            exclude_unset=True,
            id=hotel_id)
       await self.db.commit()

    async def change_hotel(
        self,
        hotel_id: int,
        hotel_data: HotelPatch = Body(),
    ):
       await self.db.hotels.update(
            model_data=hotel_data,
            exclude_unset=False,
            id=hotel_id
       )
       await self.db.commit()

    async def get_hotel_with_check(
            self,
            hotel_id: int,
    ):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex