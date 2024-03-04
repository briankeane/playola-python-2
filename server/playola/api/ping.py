from fastapi import APIRouter, Depends

from playola.config import get_settings, Settings

router = APIRouter()


@router.get("/ping")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing,
    }
