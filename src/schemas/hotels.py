from pydantic import BaseModel, Field

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    name: str | None = Field(None)

class HotelPUT(BaseModel):
    title: str
    name: str