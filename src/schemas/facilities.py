from pydantic import BaseModel,Field,ConfigDict
from datetime import date


class FacilityAdd(BaseModel):
    title: str

class Facility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityRequest(BaseModel):
    facility_id: int

class RoomFacilityAdd(BaseModel):
    room_id: int
    facility_id: int

class RoomFacility(FacilityAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)