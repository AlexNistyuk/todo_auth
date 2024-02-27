import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = os.path.join(BASE_DIR.parent.parent, ".env")


class Settings(BaseSettings):
    db_url: str
    db_pool_size: int
    db_max_overflow: int
    jwt_secret_key: str
    jwt_access_token_expires_in: int
    jwt_refresh_token_expires_in: int
    jwt_algorithm: str
    http_auth_keyword: str
    http_auth_header: str
    superuser_username: str
    superuser_password: str

    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="allow")


@lru_cache
def get_settings():
    return Settings()
