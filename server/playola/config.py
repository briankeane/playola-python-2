import logging

from pydantic_settings import BaseSettings
from functools import lru_cache
from pydantic import AnyUrl

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    database_url: AnyUrl = "DATABASE_URL"


@lru_cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
