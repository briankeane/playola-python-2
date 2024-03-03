import logging

from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import AnyUrl

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: AnyUrl = "DATABASE_URL"
    spotify_client_id: str = "THE_SPOTIFY_CLIENT_ID"
    spotify_client_secret: str = "THE_SPOTIFY_CLIENT_SECRET"
    client_base_url: str


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
