import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from httpx import AsyncClient,ASGITransport
from unittest import mock
import json

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.config import settings
from src.database import Base,engine,async_session_maker
from src.models import *
from src.main import app
from src.utils.db_manager import DBManager
from src.api.dependencies import get_db


@pytest.fixture(scope="session",autouse=True)
async def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="function")
async def db()->DBManager:
    async with (DBManager(session_factory=async_session_maker) as db):
        yield db

@pytest.fixture(scope="session",autouse=True)
async def setup_database(check_test_mode):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="session",autouse=True)
async def add_data(setup_database):

    with open("tests/mock_hotels.json",encoding="utf-8") as f:
        hotels = [
            HotelAdd(
                title=hotel['title'],
                location=hotel['location']
            )
            for hotel in json.loads(f.read())
        ]

    with open("tests/mock_rooms.json",encoding="utf-8") as f:
        rooms = [
            RoomAdd(
                hotel_id = room['hotel_id'],
                title =room['title'],
                description = room['description'],
                price = room['price'],
                quantity = room['quantity']
            )
            for room in json.loads(f.read())
        ]

    async with DBManager(session_factory=async_session_maker) as db:
        await db.hotels.add_bulk(hotels)
        await db.rooms.add_bulk(rooms)
        await db.commit()


@pytest.fixture(scope="session")
async def ac()->DBManager:
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session",autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
        "/auth/register",
        json={
            "email": "email@example.com",
            "password": "password",
        }
    )

@pytest.fixture(scope="session",autouse=True)
async def auth_ac(ac, setup_database, register_user):
    await ac.post(
        "/auth/login",
        json={
            "email": "email@example.com",
            "password": "password",
        }
    )
    assert ac.cookies.get("access_token")
    yield ac

