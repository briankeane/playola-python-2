import os

import pytest
import asyncio

from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI
from tortoise import Tortoise

from playola.main import create_application
from playola.config import get_settings, Settings


def get_settings_override():
    return Settings(testing=1, database_url=os.environ.get("DATABASE_TEST_URL"))


@pytest.fixture(scope="module")
def test_app() -> FastAPI:
    # set up
    Tortoise.init_models(["playola.models.tortoise"], "models")
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
async def test_app_with_db() -> FastAPI:
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    Tortoise.init_models(["playola.models.tortoise"], "models")
    await Tortoise.init(
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["models.tortoise"]},
    )
    await Tortoise.generate_schemas(safe=True)
    await Tortoise.close_connections()
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": ["models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.yield_fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
