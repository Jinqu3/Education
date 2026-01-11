from fastapi import Query, Body, APIRouter, HTTPException
from fastapi_cache.decorator import cache
from datetime import date

from src.exceptions import DatesCannotBeEqualException, InvalidDateOrderException, HotelNotFoundException,ObjectAlreadyExistsException
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService
from src.schemas.hotels import HotelPatch,HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Локация"),
    title: str | None = Query(None, description="Название отеля"),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-08-10"),
):
    try:
        return await HotelService(db).get_filtered_by_time(
            pagination=pagination,
            location=location,
            title= title,
            date_from=date_from,
            date_to= date_to
        )
    except DatesCannotBeEqualException as ex:
        raise HTTPException(status_code=400,detail=ex.detail)
    except InvalidDateOrderException as ex:
        raise HTTPException(status_code=400, detail=ex.detail)

@router.get("/{hotel_id}")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel(
            hotel_id=hotel_id
        )
    except HotelNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.detail)


@router.delete("/{hotel_id}")
async def delete_hotels(
    hotel_id: int,
    db: DBDep,
):
    await HotelService(db).delete_hotel(
        hotel_id=hotel_id
    )
    return {"status": "OK"}


@router.post("")
async def add_hotel(
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
    try:
        hotel = HotelService(db).add_hotel(
            hotel_data=hotel_data,
        )
    except ObjectAlreadyExistsException:
        raise HTTPException(status_code=409,detail="Отель не найден")
    return {"status": "OK", "data": hotel}


@router.patch("/{hotel_id}")
async def change_hotel_parts(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch = Body(),
):
    await HotelService(db).change_hotel_parts(
        hotel_id=hotel_id,
        hotel_data=hotel_data
        )
    return {"status": "OK"}


@router.put("/{hotel_id}")
async def change_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelAdd = Body(),
):
    await HotelService(db).change_hotel(
        hotel_id=hotel_id,
        hotel_data=hotel_data
    )
    return {"status": "OK"}
