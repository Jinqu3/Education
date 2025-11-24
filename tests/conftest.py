import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from httpx import AsyncClient,ASGITransport
import json

from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.config import settings
from src.database import Base,engine_null_pool,async_session_maker_null_pool
from src.models import *
from src.main import app
from src.utils.db_manager import DBManager




@pytest.fixture(scope="session",autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session",autouse=True)
async def async_main(check_test_mode):

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session",autouse=True)
async def add_data(async_main):

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        with open("tests/mock_hotels.json",encoding="utf-8") as f:
            data = [HotelAdd(title=hotel['title'], location=hotel['location']) for hotel in json.loads(f.read())]
            await db.hotels.add_bulk(data)
            await db.commit()

        with open("tests/mock_rooms.json",encoding="utf-8") as f:
            data = [
                RoomAdd(
                    hotel_id = room['hotel_id'],
                    title =room['title'],
                    description = room['description'],
                    price = room['price'],
                    quantity = room['quantity']
                )
                for room in json.loads(f.read())
            ]
            await db.rooms.add_bulk(data)
            await db.commit()


@pytest.fixture(scope="session",autouse=True)
async def register(async_main):
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as client:
        await client.post(
            "/auth/register",
            json={
                "email": "email",
                "password": "password",
            }
        )
