from pydantic import BaseModel, Field

class HotelPatch(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)

class Hotel(BaseModel):
    title: str
    location: str