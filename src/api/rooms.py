from fastapi import APIRouter,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.rooms import RoomAdd, RoomPatch
from src.database import async_session_maker
from src.repository.rooms import RoomsRepository
from src.api.dependencies import UserIdDep


router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Комнаты"])

@router.get("")
async def get_rooms(
    hotel_id: int,
):
    async with async_session_maker() as session:
        try:
            rooms = await RoomsRepository(session).get_all(hotel_id=hotel_id)
        except Exception as e:
            raise HTTPException(401, detail=f"Не возможно получить список номеров {e}")
        return {"rooms": rooms}

@router.get("/{room_id}")
async def get_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        try:
            room = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)
            if room is None:
                raise HTTPException(404, detail="Номер не найден")
        except Exception as e:
            raise HTTPException(401, detail=f"Не возможно получить номер: {e}")
        return {"room": room}


@router.post("")
async def create_room(
    room_data: RoomAdd,
):
    async with async_session_maker() as session:
        try:
           room =  await RoomsRepository(session).add(room_data)
        except Exception as e:
            raise HTTPException(401, detail=f"Ошибка при создании номера: {e}")
        await session.commit()
        return {"room": room}

@router.delete("/{room_id}")
async def delete_room(
    room_id: int,
    hotel_id: int,
):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).delete(id = room_id,hotel_id = hotel_id)
        except Exception as e:
            raise HTTPException(401, detail=f"Не возможно удалить номер: {e}")
        return {"status": "OK"}


@router.put("/{room_id}")
async def change_room(
    model_data: RoomAdd,
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).update(model_data,False,id = room_id,hotel_id = hotel_id)
        except Exception as e:
            raise HTTPException(401, detail=f"Не возможно изменить номер: {e}")
        await session.commit()
        return {"status": "OK"}

@router.patch("/{room_id}")
async def change_room(
    model_data: RoomPatch,
    hotel_id: int,
    room_id: int,
):
    async with async_session_maker() as session:
        try:
            await RoomsRepository(session).update(model_data,True,id = room_id,hotel_id = hotel_id)
        except Exception as e:
            raise HTTPException(401, detail=f"Не возможно изменить номер: {e}")
        await session.commit()
        return {"status": "OK"}