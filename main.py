from pydantic import Field
from fastapi import FastAPI, Query, Body, HTTPException
import uvicorn
from fastapi.routing import APIRoute
from pydantic import BaseModel

# app = FastAPI(docs_url=None)
app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@app.get("/hotels")
def get_hotels(
        id : int | None = Query(default=None,description="Айди"),
        title : str | None = Query(default=None,description="Название отеля"),
        page:int | None = 1,
        per_page:int | None = 3,
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_[(page-1) * per_page : (page-1) * per_page + per_page]

@app.delete("/hotels/{hotel_id}")
def delete_hotels(
    hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": 200, "hotels": hotels}

@app.post("/hotels")
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


# Модель для частичного обновления
class HotelUpdate(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)

class HotelReplace(BaseModel):
    title: str
    name: str

@app.patch("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    update_data : HotelUpdate,
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

@app.patch("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    update_data : HotelUpdate,
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

@app.put("/hotels/{hotel_id}")
def change_hotel(
    hotel_id: int,
    update_data : HotelReplace,
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


import time,asyncio

@app.get("/sync/{id}")
def sync_func(id:int):
    print(f"sync начал {id}:{time.time():.2f}")
    time.sleep(3)
    print(f"sync закончил {id}:{time.time():.2f}")


@app.get("/async/{id}")
async def async_func(id:int):
    print(f"async начал {id}:{time.time():.2f}")
    await asyncio.sleep(3)
    print(f"async закончил {id}:{time.time():.2f}")





if __name__ == "__main__":
    uvicorn.run("main:app",port=8000)