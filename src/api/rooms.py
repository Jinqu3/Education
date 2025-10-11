from fastapi import APIRouter,HTTPException,Body,Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date


from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.database import async_session_maker
from src.repository.rooms import RoomsRepository
from src.api.dependencies import UserIdDep,DBDep


router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-01")
):
    try:
        rooms = await db.rooms.get_filtered_by_time(hotel_id=hotel_id,date_from=date_from,date_to=date_to)
    except Exception as e:
        raise HTTPException(404, detail=f"Не возможно получить список номеров")
    return {"rooms": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        room = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)
    except Exception as e:
        raise HTTPException(404, detail=f"Не возможно получить номер")
    return {"room": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAdd = Body(),
):
    try:
       room =  await db.rooms.add(room_data)
       await session.commit()
    except Exception as e:
        raise HTTPException(404, detail=f"Ошибка при создании номера:")
    return {"room": room}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
):
    try:
        await db.rooms.delete(id = room_id,hotel_id = hotel_id)
    except Exception as e:
        raise HTTPException(401, detail=f"Не возможно удалить номер: {e}")
    return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomAdd = Body(),
):

    try:
        await db.rooms.update(room_data,False,id = room_id,hotel_id = hotel_id)
        await db.commit()
    except Exception as e:
        raise HTTPException(404, detail=f"Не возможно изменить номер:")
    return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room(
    db:DBDep,
    hotel_id: int,
    room_id: int,
    room_data: RoomPatch = Body(),
):
    try:
        await db.rooms.update(room_data,True,id = room_id,hotel_id = hotel_id)
        await db.commit()
    except Exception as e:
        raise HTTPException(404, detail=f"Не возможно изменить номер:")
    return {"status": "OK"}