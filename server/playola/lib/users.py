from spotipy import oauth2, Spotify

from fastapi import Depends
from playola.models.tortoise import User
from playola.config import Settings, get_settings


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


async def get_or_create_user_from_spotify_code(code: str, 
                                               settings: Settings = Depends(get_settings)):
  sp_oauth = oauth2.SpotifyOAuth(
        settings.spotify_client_id,
        settings.spotify_client_secret,
        f"{settings.base_url}/v1/auth/spotify/code",
        scope=scopes,
    )
  token_info = sp_oauth.get_access_token(code, check_cache=False)
  sp = Spotify(auth=token_info["access_token"])
  user = sp.current_user()
  (user, created) = await User.get_or_create(
    spotify_user_id=user["id"],
      defaults={
          "spotify_token_info": token_info,
          "spotify_display_name": user["display_name"],
      },
  )
  return user
