from fastapi import APIRouter, HTTPException, Body, Query
from datetime import date

from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.api.dependencies import DBDep
from src.exceptions import DatesCannotBeEqualException,InvalidDateOrderException,CanNotAddObjectException,ObjectNotFoundException

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    try:
        rooms = await db.rooms.get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )
    except DatesCannotBeEqualException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    except InvalidDateOrderException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    return {"data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        room = await db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)
    except ObjectNotFoundException:
        raise HTTPException(404, detail="Не возможно получить номер")
    return {"data": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    try:
        room = await db.rooms.add(_room_data)
    except CanNotAddObjectException:
        raise HTTPException(404, detail="Невозможно забронировать номер")

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    except CanNotDeleteObjectException:
        raise HTTPException(401, detail="Не возможно удалить номер:")
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(),
):
    try:
        _room_data = RoomAdd(**room_data.model_dump(exclude={"facilities_ids"}))
        await db.rooms.update(_room_data, False, id=room_id, hotel_id=hotel_id)
        await db.rooms_facilities.set_room_facilities(
            room_id, facility_ids=room_data.facilities_ids
        )
        await db.commit()
    except CanNotСhangeObjectException:
        raise HTTPException(404, detail="Не возможно изменить номер")
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room_parts(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(),
):
    try:
        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch(hotel_id=hotel_id, **_room_data_dict)
        await db.rooms.update(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
        if "facilities_ids" in _room_data_dict:
            await db.rooms_facilities.set_room_facilities(
                room_id, facilities_ids=room_data.facilities_ids
            )
        await db.commit()
    except CanNotСhangeObjectException:
        raise HTTPException(404, detail="Не возможно изменить номер")
    return {"status": "OK"}
