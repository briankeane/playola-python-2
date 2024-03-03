from unittest.mock import AsyncMock
import pytest

from fastapi import Depends
from playola.config import Settings, get_settings
from playola.api.spotify_auth import *

from playola.models.tortoise import User

def test_ping(test_app):
    response = test_app.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong!", "testing": True}

