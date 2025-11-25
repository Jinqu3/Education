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
    new_booking = await db.bookings.add(booking_data)
    await db.commit()

    #READ
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert new_booking
    assert booking.user_id == new_booking.id
    assert booking.room_id == new_booking.room_id
    assert booking.date_from == new_booking.date_from
    assert booking.date_to == new_booking.date_to
    assert booking.price == new_booking.price


    find_all_bookings = await db.bookings.get_all()
    assert find_all_bookings

    #UPDATE
    update_booking_data = BookingAdd(
        user_id=test_user,
        room_id=test_room,
        date_from=date(2024, 1, 10),
        date_to=date(2024, 1, 15),
        price=100
    )

    await db.bookings.update(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == date(2024, 1, 15)

    #DELETE
    await db.bookings.delete(id = booking.id)
    find_deleted_booking = await db.bookings.get_one_or_none(id=booking.id)
    assert not find_deleted_booking

    await db.rollback()

