from fastapi import Query,Body, APIRouter
from sqlalchemy import insert, select, column

from src.schemas.hotels import Hotel,HotelPatch
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.repository.hotels import HotelRepository

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title:str | None = Query(None,description="Hotel Title"),
        location:str | None = Query(None,description="Hotel Location"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            location = location,
            title = title,
            limit=per_page,
            offset=pagination.per_page * (pagination.page-1)
        )

@router.get("/{hotel_id}")
async def get_hotel(
    hotel_id: int,
):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotels(
    hotel_id:int
):
    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        return {"status": 200}

@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(
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
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()
        return {"status": 200,"data":hotel}


@router.patch("/{hotel_id}")
async def change_hotel(
    hotel_id:int,
    hotel_data: HotelPatch = Body(),
):
    async with async_session_maker() as session:
        await HotelRepository(session).update(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        return {"status": 200}

@router.put("/{hotel_id}")
async def change_hotel(
    hotel_id:int,
    hotel_data: Hotel = Body(),
):
    async with async_session_maker() as session:
        await HotelRepository(session).update(hotel_data,exclude_unset = False, id=hotel_id)
        await session.commit()
        return {"status": 200}

