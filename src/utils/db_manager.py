from database import async_session_maker
from repository.hotels import HotelsRepository
from repository.rooms import RoomsRepository
from repository.users import UsersRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = session_factory()

        self.hotels = HotelRepository(self.session)
        self.rooms = RoomsRepository(self.session)
        self.users = UsersRepository(self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        self.session.commit()