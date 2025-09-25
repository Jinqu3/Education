from src.repository.base import BaseRepository
from src.models.rooms import RoomsORM
from src.schemas.rooms import Room
from sqlalchemy import select

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room
