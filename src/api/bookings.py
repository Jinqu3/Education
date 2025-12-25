from datetime import date
from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import UserIdDep,DBDep
from src.schemas.bookings import Booking,BookingAddRequest,BookingAdd
from src.models.bookings import BookingsORM

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body()
):
    # Расчёт суммы бронирования
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    days = (booking_data.date_to - booking_data.date_from).days
    price = days * room_price

    _booking_data = BookingAdd(user_id=user_id,price=price,**booking_data.model_dump())
    booking = await db.bookings.add_booking(_booking_data,hotel_id=room.hotel_id)
    await db.commit()

    return {"status": 200, "data": booking}


@router.get("")
async def get_bookings(
        db: DBDep
):
    try:
        return await db.bookings.get_all()
    except:
        raise HTTPException(404,detail="Непредвиденная ошибка")

@router.get("/me")
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep
):
    try:
        return await db.bookings.get_filtered(user_id=user_id)
    except:
        raise HTTPException(404,detail="Непредвиденная ошибка")
