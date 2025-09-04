from fastapi import Query,Body, APIRouter
from sqlalchemy import insert, select, column

from src.schemas.hotels import Hotel,HotelPatch
from src.api.dependencies import PaginationDep
from database import async_session_maker
from src.models.hotels import HotelsORM

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title:str | None = Query(None,description="Hotel Title"),
        location:str | None = Query(None,description="Hotel Location"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsORM)
        if title:
            query = query.where(column("title").like(f"%{title}%"))
        if location:
            query = query.where(column("location").like(f"%{location}%"))
            print(query)
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page -1))
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels



@router.delete("/{hotel_id}")
def delete_hotels(
):
    pass

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
        add_hotel_statement = insert(HotelsORM).values(**hotel_data.model_dump())
        await session.execute(add_hotel_statement)
        await session.commit()
        return {"status": 200}




@router.patch("/{hotel_id}")
def change_hotel(
):
    pass

@router.put("/{hotel_id}")
def change_hotel(
):
   pass

