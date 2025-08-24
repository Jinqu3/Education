from fastapi import FastAPI, Query, Body, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn
from fastapi.routing import APIRoute
from pydantic import BaseModel

# app = FastAPI(docs_url=None)
app = FastAPI()

hotels = [
    {"id": 1, "city": "Воронеж", "country":"Россия"},
    {"id": 2, "city": "Сочи","country":"Россия"},
    {"id": 3 ,"city": "Париж","country":"Франция"},
]

@app.get("/hotels")
def get_hotels(
        id : int | None = Query(default=None,description="Айди"),
        city : str | None = Query(default=None,description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if city and hotel["city"] != city:
            continue
        hotels_.append(hotel)
    return hotels_

@app.delete("/hotels/{hotel_id}")
def delete_hotels(
    hotel_id: int
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": 200, "hotels": hotels}

@app.post("/hotels")
def create_hotel(
    city: str = Body(embed=True),
    country: str = Body(embed=True),
):
    global hotels
    hotels.append(
        {
            "id": hotels[-1]["id"]+1,
            "city":city,
            "country":country,
        }
    )
    return {"status": 200, "hotels": hotels}


# Модель для частичного обновления
class HotelUpdate(BaseModel):
    city: str | None = None
    country: str | None = None

class HotelReplace(BaseModel):
    city: str
    country: str

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







# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         city=app.city + " - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
#         swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
#     )


if __name__ == "__main__":
    uvicorn.run("main:app")