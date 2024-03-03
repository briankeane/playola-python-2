import os

from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise

from playola.config import get_settings, Settings
from playola.api import ping

app = FastAPI()

def create_application() -> FastAPI:
    application = FastAPI()

    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["playola.models.tortoise"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )

    application.include_router(ping.router, prefix="/api/v1")
    return application

app = create_application()
