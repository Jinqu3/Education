from src.repository.bookings import BookingsRepository
from src.repository.hotels import HotelsRepository
from src.repository.rooms import RoomsRepository
from src.repository.users import UsersRepository
from src.repository.facilities import FacilityRepository,RoomFacilityRepository



class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.hotels = HotelsRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)
        self.bookings = BookingsRepository(self.session)
        self.facilities = FacilityRepository(self.session)
        self.rooms_facilities = RoomFacilityRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()