from datetime import date
from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import UserIdDep,DBDep
from src.models.facilities import FacilitiesORM
from src.schemas.facilities import FacilityAdd,RoomFacilityAdd,RoomFacilityRequest

router = APIRouter(prefix="/facilities", tags=["Особенности"])

@router.get("/{room_id}")
async def get_room_facilities(
    room_id: int,
    db: DBDep,
):
    return await db.rooms_facilities.get_filtered(room_id=room_id)

@router.get("")
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()


@router.delete("/{room_id}/{facility_id}")
async def delete_room_facilities(
    room_id:int,
    facility_id: int,
    db: DBDep,
):
    await db.rooms_facilities.delete(room_id=room_id,facility_id=facility_id)
    return {"status": 200}

@router.delete("/{facility_id}")
async def delete_facilities(
    facility_id:int,
    db: DBDep,
):
    await db.rooms_facilities.delete(id=facility_id)
    return {"status": 200}

@router.post("/{room_id}")
async def create_room_facility(
    db: DBDep,
    room_id: int,
    room_facility_data : RoomFacilityRequest,
):
    room_facility_data = RoomFacilityAdd(room_id=room_id,**room_facility_data.model_dump())
    print(room_facility_data)
    room_facility = await db.rooms_facilities.add(room_facility_data)
    await db.commit()
    return {"status": 200,"data":room_facility}

@router.post("")
async def create_facility(
    db: DBDep,
    facility_data : FacilityAdd,
):
    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": 200,"data":facility}