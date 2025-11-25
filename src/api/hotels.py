from fastapi import Query,Body, APIRouter
from datetime import date
from fastapi_cache.decorator import cache

from src.schemas.hotels import Hotel,HotelPatch,HotelAdd
from src.api.dependencies import PaginationDep,DBDep
from src.database import async_session_maker

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db:DBDep,
        location: str | None = Query(None, description="Локация"),
        title: str | None = Query(None, description="Название отеля"),
        date_from: date = Query(example="2024-08-01"),
        date_to: date = Query(example="2024-08-10"),
):
    per_page = pagination.per_page or 10
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotels(
    hotel_id:int,
    db: DBDep,
):
    await db.hotels.delete(id=hotel_id)
    return {"status": 200}

@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Сочи",
                "value": {
                    "title": "Отель 5 звезд у моря",
                    "location": "Сочи, ул. Моря, 1",
                },
            },
            "2": {
                "summary": "Дубай",
                "value": {
                    "title": "Отель  У фонтана",
                    "location": "Дубай, ул. Шейха, 2",
                },
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": 200,"data":hotel}


@router.patch("/{hotel_id}")
async def change_hotel(
    db: DBDep,
    hotel_id:int,
    hotel_data: HotelPatch = Body(),
):
    await db.hotels.update(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": 200}

@router.put("/{hotel_id}")
async def change_hotel(
    db: DBDep,
    hotel_id:int,
    hotel_data: HotelAdd = Body(),
):
    await db.hotels.update(hotel_data,exclude_unset = False, id=hotel_id)
    await db.commit()
    return {"status": 200}

