from fastapi import APIRouter, HTTPException, Body, Query
from datetime import date


from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.api.dependencies import DBDep
from src.exceptions import DatesCannotBeEqualException, InvalidDateOrderException, \
    RoomNotFoundException, RoomNotFoundHTTPException, HotelNotFoundException, HotelNotFoundHTTPException
from src.services.rooms import RoomService

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    try:
        return await RoomService(db).get_filtered_by_time(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to,
        )
    except DatesCannotBeEqualException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    except InvalidDateOrderException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        return await RoomService(db).get_room(
            hotel_id=hotel_id,
            room_id=room_id,
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(),
):
    try:
        room = await RoomService(db).add_room(
            hotel_id=hotel_id,
            room_data=room_data,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status":"OK", "data": room}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    await RoomService(db).delete_room(
        hotel_id=hotel_id,
        room_id=room_id,
    )
    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(),
):
    try:
        await RoomService(db).change_room(
            hotel_id=hotel_id,
            room_id=room_id,
            room_data=room_data,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room_parts(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(),
):
    try:
        await RoomService(db).change_room(
            hotel_id=hotel_id,
            room_id=room_id,
            room_data=room_data,
        )
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    return {"status": "OK"}
