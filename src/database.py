from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import NullPool
from src.config import settings
from sqlalchemy.orm import DeclarativeBase

db_params = {}
if settings.MODE == "TEST":
    db_params = {"poolclass": NullPool}

engine = create_async_engine(settings.DB_URL, **db_params)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
