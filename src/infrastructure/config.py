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
    jwt_secret_key: str
    jwt_access_token_expires_in: int
    jwt_refresh_token_expires_in: int
    jwt_algorithm: str
    http_auth_keyword: str
    http_auth_header: str

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH)


@lru_cache
def get_settings():
    return Settings()
