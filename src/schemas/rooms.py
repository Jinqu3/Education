from pydantic import BaseModel,Field

class RoomPatch(BaseModel):
    hotel_id: int
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)

class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str= Field(None)
    price: int
    quantity: int


class Room(RoomAdd):
    id: int