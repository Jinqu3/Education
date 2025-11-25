from src.schemas.bookings import BookingAdd
from datetime import date


async def test_booking_crud(db):

    #CREATE
    test_user = (await db.users.get_all())[0].id
    test_room = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=test_user,
        room_id=test_room,
        date_from=date(2024,1,10),
        date_to=date(2024,1,11),
        price=100
    )
    booking = await db.bookings.add(booking_data)
    assert booking
    await db.commit()

    #READ
    find_booking_with_id = await db.bookings.get_one_or_none(id=booking.id)
    assert find_booking_with_id

    find_all_bookings = await db.bookings.get_all()
    assert find_all_bookings

    #DELETE
    await db.bookings.delete(id = booking.id)
    find_deleted_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert not find_deleted_booking

