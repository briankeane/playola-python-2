from unittest.mock import AsyncMock

from playola.models.tortoise import User
from playola.config import get_settings


def test_spotify_code_success(test_app, mocker):
    user = User(
        spotify_token_info={
            "access_token": "THE ACCESS_TOKEN",
            "refresh_token": "THE_REFRESH_TOKEN",
        },
        spotify_user_id="the_spotify_user_id",
        spotify_display_name="the_display_name",
    )
    future = AsyncMock(return_value=user)
    mocker.patch(
        "playola.api.spotify_auth.get_or_create_user_from_spotify_code",
        side_effect=future,
    )
    code = "aasdfasdf"
    response = test_app.get(f"/api/v1/spotify/code?code={code}", allow_redirects=False)

    future.assert_awaited_once_with(code)
    assert response.status_code == 302
    assert (
        response.headers["location"]
        == f"{get_settings().client_base_url}/users/the_spotify_user_id"
    )
