from datetime import date
from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import UserIdDep,DBDep
from src.schemas.bookings import Booking,BookingAddRequest,BookingAdd
from src.models.bookings import BookingsORM

router = APIRouter(prefix="/bookings", tags=["Бронирования"])

@router.post("")
async def create_bookings(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingAddRequest = Body()
):
    # Расчёт суммы бронирования
    try:
        room_price = await db.rooms.get_one_or_none(id=booking_data.room_id)
        days = (booking_data.date_to - booking_data.date_from).days
        price = days * room_price.price
    except:
        raise HTTPException(status_code=400,detail="Невозможно расчитать сумму бронирования")
    try:
        booking_data = BookingAdd(user_id=user_id,price=price,**booking_data.model_dump())
        booking = await db.bookings.add(booking_data)
        await db.commit()
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))
    return {"status": 200, "data": booking}

