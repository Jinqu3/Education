from fastapi import APIRouter, Body,HTTPException

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.exceptions import ObjectNotFoundException,AllRoomsAreBookedException

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingAddRequest = Body()):
    # Расчёт суммы бронирования
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404,detail="Номер не найден")
    room_price = room.price
    days = (booking_data.date_to - booking_data.date_from).days
    price = days * room_price

    _booking_data = BookingAdd(user_id=user_id, price=price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409,detail=ex.detail)
    await db.commit()

    return {"data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)
