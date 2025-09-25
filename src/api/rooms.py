from fastapi import APIRouter,HTTPException,Body
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatch, RoomPatchRequest
from src.database import async_session_maker
from src.repository.rooms import RoomsRepository
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/hotels", tags=["Номера"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
    hotel_id: int,
):
    async with async_session_maker() as session:
        try:
            rooms = await RoomsRepository(session).get_filtered(hotel_id=hotel_id)
        except Exception as e:
            raise HTTPException(404, detail=f"Не возможно получить список номеров")
        return {"rooms": rooms}

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        try:
            room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
        except Exception as e:
            raise HTTPException(404, detail=f"Не возможно получить номер")
        return {"room": room}


@router.post("/{hotel_id}/rooms")
async def create_room(
    hotel_id: int,
    room_data: RoomAddRequest = Body(),
):
    room_data = RoomAdd(hotel_id = hotel_id, **room_data.model_dump())

    async with async_session_maker() as session:
        try:
           room =  await RoomsRepository(session).add(room_data)
           await session.commit()
        except Exception as e:
            raise HTTPException(404, detail=f"Ошибка при создании номера:")
        return {"room": room}

@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).delete(id = room_id,hotel_id = hotel_id)
        except Exception as e:
            raise HTTPException(401, detail=f"Не возможно удалить номер: {e}")
        return {"status": "OK"}


@router.put("/{hotel_id}/rooms/{room_id}")
async def change_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomAddRequest = Body(),
):

    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).update(room_data,False,id = room_id,hotel_id = hotel_id)
            await session.commit()
        except Exception as e:
            raise HTTPException(404, detail=f"Не возможно изменить номер:")
        return {"status": "OK"}

@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest = Body(),
):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).update(room_data,True,id = room_id,hotel_id = hotel_id)
            await session.commit()
        except Exception as e:
            raise HTTPException(404, detail=f"Не возможно изменить номер:")
        return {"status": "OK"}