from src.repository.base import BaseRepository
from src.models.facilities import RoomsFacilitiesORM,FacilitiesORM
from src.schemas.facilities import Facility,RoomFacility

class FacilityRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facility

class RoomFacilityRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility