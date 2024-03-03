import os
import logging

from fastapi import FastAPI

from contextlib import asynccontextmanager
from playola.api import ping, spotify_auth
from playola.db import init_db


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, prefix="/api/v1")
    application.include_router(spotify_auth.router, prefix="/api/v1/spotify", tags=["spotify_auth"])

    return application


app = create_application()

# Note: 
#    -- replace this when tortoise-orm adds support for
#       lifespan methods
#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Load the ML model
#     log.info("Starting up...")
#     init_db(app)
#     yield
#     # Clean up the ML models and release the resources
#     log.info("Shutting down...")

@app.on_event("startup")
async def startup_event():
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
