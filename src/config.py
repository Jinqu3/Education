from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DB_NAME:str
    DB_HOST:str
    DB_PORT:int
    DB_PASS:str
    DB_USER:str

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()
