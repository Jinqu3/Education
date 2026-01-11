from fastapi import APIRouter, Body,HTTPException

from exceptions import RoomNotFoundHTTPException
from src.api.dependencies import UserIdDep, DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException, AllRoomsAreBookedHTTPException, ObjectAlreadyExistsException, \
    RoomNotFoundException, HotelNotFoundException
from src.services.bookings import BookingService

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest = Body()
):
    try:
        booking = await BookingService(db).add_booking(
            user_id=user_id,
            booking_data=booking_data
        )
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except AllRoomsAreBookedException:
        raise AllRoomsAreBookedHTTPException

    return {"status":"OK","data": booking}


@router.get("")
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me")
async def get_my_bookings(
        user_id: UserIdDep,
        db: DBDep
):
    return await BookingService(db).get_my_bookings(user_id=user_id)

