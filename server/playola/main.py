import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from playola.api import ping, spotify_auth, users
from playola.db import init_db


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, prefix="/api/v1")
    application.include_router(
        spotify_auth.router, prefix="/api/v1/auth/spotify", tags=["spotify_auth"]
    )
    application.include_router(users.router, prefix="/api/v1/users", tags=["users"])

    origins = [
        "http://localhost:3000",
        "https://localhost:3000",
        "https://admin.playola.fm",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


app = create_application()


# Note:
#    -- remove this when tortoise-orm adds support for
#       lifespan methods
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    log.info("Starting up...")
    init_db(app)
    yield
    # Clean up the ML models and release the resources
    log.info("Shutting down...")


@app.on_event("startup")
async def startup_event():
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
