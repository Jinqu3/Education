from fastapi import Query, Body, HTTPException, APIRouter
from src.schemas.hotels import HotelPUT,HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get("/hotels")
def get_hotels(
        pagination: PaginationDep,
        id : int | None = Query(default=None,description="Айди"),
        title : str | None = Query(default=None,description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[(pagination.page-1) * pagination.per_page :(pagination.page-1) * pagination.per_page + pagination.per_page]

@router.delete("/hotels/{hotel_id}")
def delete_hotels(
    hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": 200, "hotels": hotels}

@router.post("/hotels")
def create_hotel(
    title: str = Body(embed=True),
    name: str = Body(embed=True),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"]+1,
            "title":title,
            "name":name,
        }
    )
    return {"status": 200, "hotels": hotels}




@router.patch("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    update_data : HotelPatch,
):
    hotel_to_update = None
    for i,val in enumerate(hotels):
        if hotels[i]["id"] == hotel_id:
            hotel_to_update = hotels[i]
            break

    if not hotel_to_update:
        raise HTTPException(status_code=404, detail="Отель не найден")

    update_dict = update_data.model_dump(exclude_unset=True)
    print(f"update_dict: {update_dict}")


    for field, value in update_dict.items():
        hotel_to_update[field] = value

    return {"status": 200, "hotels": hotels}

@router.put("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    update_data : HotelPUT,
):
    hotel_to_update = None
    for i,val in enumerate(hotels):
        if hotels[i]["id"] == hotel_id:
            hotel_to_update = hotels[i]
            break


    if not hotel_to_update:
        raise HTTPException(status_code=404, detail="Отель не найден")

    update_dict = update_data.model_dump()

    for field, value in update_dict.items():
        hotel_to_update[field] = value

    return {"status": 200, "hotels": hotels}


# import time,asyncio
#
# @router.get("/sync/{id}")
# def sync_func(id:int):
#     print(f"sync начал {id}:{time.time():.2f}")
#     time.sleep(3)
#     print(f"sync закончил {id}:{time.time():.2f}")
#
#
# @router.get("/async/{id}",)
# async def async_func(id:int):
#     print(f"async начал {id}:{time.time():.2f}")
#     await asyncio.sleep(3)
#     print(f"async закончил {id}:{time.time():.2f}")

