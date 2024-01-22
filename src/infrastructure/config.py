import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = os.path.join(BASE_DIR.parent.parent, ".env")


class Settings(BaseSettings):
    web_host: str
    web_port: int
    web_container_host: str
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    db_url: str

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)


@lru_cache
def get_settings():
    return Settings()
