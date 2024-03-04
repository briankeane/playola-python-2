from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from playola.config import Settings, get_settings
from playola.models.pydantic import SpotifyCodePayloadSchema
from playola.lib.users import get_or_create_user_from_spotify_code
from spotipy import oauth2
from starlette import status

router = APIRouter()

scopes = ",".join(
    [
        "playlist-read-collaborative",
        "user-follow-read",
        "user-read-playback-position",
        "user-top-read",
        "user-read-recently-played",
        "user-library-read",
        "user-read-email",
        "user-read-currently-playing",
        "user-modify-playback-state",
        "user-read-playback-state",
    ]
)


# this is where the user is redirected after signing into spotify.
# we exchange the code for a token_info and redirect the user to
# their page.
@router.get("/code")
async def spotify_auth_code(
    payload: SpotifyCodePayloadSchema = Depends(),
    settings: Settings = Depends(get_settings),
):
    user = await get_or_create_user_from_spotify_code(payload.code)
    return RedirectResponse(
        f"{settings.client_base_url}/users/{user.spotify_user_id}",
        status_code=status.HTTP_302_FOUND,
    )


# redirects the user to spotify to sign in... then to /code with a "code"
# that we exchange for a token_info
@router.get("/authorize")
async def spotify_auth_redirect(settings: Settings = Depends(get_settings)):
    sp_oauth = oauth2.SpotifyOAuth(
        settings.spotify_client_id,
        settings.spotify_client_secret,
        f"{settings.base_url}/v1/auth/spotify/code",
        scope=scopes,
    )

    return RedirectResponse(
        sp_oauth.get_authorize_url(), status_code=status.HTTP_302_FOUND
    )
