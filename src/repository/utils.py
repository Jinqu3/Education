from src.models.bookings import BookingsORM
from src.models.rooms import RoomsORM

from sqlalchemy import select,func
from datetime import date
from src.database import engine


async def rooms_ids_for_booking(
        hotel_id: int | None,
        date_from: date,
        date_to: date
):
    """
    with rooms_count as (
        select room_id, count(*) as rooms_booked from bookings
        where date_from <= '2024-11-07' and date_to >= '2024-07-01'
        group by room_id
    ),
    rooms_left_table as (
        select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
        from rooms
        left join rooms_count on rooms.id = rooms_count.room_id
    )
    select * from rooms_left_table
    where rooms_left > 0;
    """

    rooms_count = (
        select(BookingsORM.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsORM)
        .filter(
            BookingsORM.date_from <= date_to,
            BookingsORM.date_to >= date_from,
        )
        .group_by(BookingsORM.room_id)
        .cte(name="rooms_count")
    )

    rooms_ids_for_hotel = (
        select(RoomsORM.id)
        .select_from(RoomsORM)
    )

    if hotel_id is not None:
        rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel = (
        rooms_ids_for_hotel
        .subquery(name="rooms_ids_for_hotel")
    )

    rooms_left_table = (
        select(
            RoomsORM.id.label("room_id"),
            (RoomsORM.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsORM)
        .outerjoin(rooms_count, RoomsORM.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )


    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(rooms_ids_for_hotel)
        )
    )

    return await self.get_filtered(RoomsORM.id.in_(rooms_ids_to_get))
