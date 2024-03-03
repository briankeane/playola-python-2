from playola.models.tortoise import User

def test_ping(test_app):
    response = test_app.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.json() == {"environment": "dev", "ping": "pong!", "testing": True}

def test_spotify_code(test_app, mock_get_or_create_user_via_token):
    user = User(spotify_token_info={"access_token": "THE ACCESS_TOKEN", "refresh_token": "THE_REFRESH_TOKEN"},
        spotify_user_id="the_spotify_user_id",
        spotify_display_name="the_display_name")
    mock_get_or_create_user_via_token.return_value = user

    response = test_app.get("/api/v1/spotify/code?code=aasdfasdf")
    assert response == {}
