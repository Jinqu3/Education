from fastapi import Body

from exceptions import ObjectNotFoundException
from src.services.base import BaseService
from src.schemas.facilities import FacilityAdd

class FacilitiesService(BaseService):

    async def get_facilities(self):
        return await self.db.facilities.get_all()

    async def get_facility(
        self,
        facility_id: int,
    ):
        try:
             facility = await self.db.facilities.get_one_or_none(id=facility_id)
        except ObjectNotFoundException as ex:
            raise FacilityNotFoundException from ex
        return facility

    async def add_facility(
        self,
        facility_data: FacilityAdd = Body(),
    ):
        facility = await self.db.facilities.add(facility_data)
        await self.db.commit()
        return facility

    async def delete_facility(
        self,
        facility_id: int,
    ):
        await self.db.rooms_facilities.delete(id=facility_id)
        await self.db.commit()