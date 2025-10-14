from datetime import date
from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import UserIdDep,DBDep
from src.models.facilities import FacilitiesORM
from src.schemas.facilities import FacilityAdd,RoomFacilityAdd

router = APIRouter(prefix="/facilities", tags=["Особенности"])

@router.get("")
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()

@router.get("{facility_id}")
async def get_facilities(
    db: DBDep,
    facility_id: int,
):
    return await db.facilities.get_one_or_none(facility_id=facility_id)


@router.delete("/{facility_id}")
async def delete_facilities(
    facility_id:int,
    db: DBDep,
):
    await db.rooms_facilities.delete(id=facility_id)
    return {"status": 200}


@router.post("")
async def create_facility(
    db: DBDep,
    facility_data : FacilityAdd = Body(),
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": 200,"data":facility}