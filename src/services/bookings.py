from datetime import date
from idlelib.autocomplete import TRY_A

from fastapi import Body

from src.exceptions import RoomNotFoundException, HotelNotFoundException,ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAddRequest,BookingAdd
from src.api.dependencies import UserIdDep
from src.services.base import BaseService
from src.services.rooms import RoomService
from src.services.hotels import HotelService

class BookingService(BaseService):

    async def add_booking(
        self,
        user_id: UserIdDep,
        booking_data: BookingAddRequest = Body()
    ):
        # Расчёт суммы бронирования
        try:
            room = await RoomService(self.db).get_room(room_id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex

        try:
            await HotelService(self.db).get_hotel(hotel_id=room.hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex

        final_price = await self.calculate_price(
            price_for_one_day = room.price,
            date_from=  booking_data.date_from,
            date_to = booking_data.date_to
        )

        _booking_data = BookingAdd(user_id=user_id, price=final_price, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
        except AllRoomsAreBookedException as ex:
            raise AllRoomsAreBookedException from ex
        await self.db.commit()

        return booking

    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(
        self,
        user_id: UserIdDep,
    ):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def calculate_price(
        self,
        price_for_one_day: int,
        date_from: date,
        date_to: date,
    ):
        days = (date_to - date_from).days
        final_price = days * price_for_one_day

        return final_price