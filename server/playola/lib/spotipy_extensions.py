from playola.config import get_settings
from playola.models.tortoise import User
from spotipy import CacheHandler, Spotify, SpotifyOAuth


class UserSpecificCacheHandler(CacheHandler):
    def __init__(self, user):
        self.user = user

    def get_cached_token(self):
        print("getting cached info", self.user.spotify_token_info)
        return self.user.spotify_token_info

    def save_token_to_cache(self, token_info):
        print("saving token info: ", token_info)
        self.user.spotify_token_info = token_info
        self.user.save()


class UserSpecificSpotify(Spotify):
    def __init__(self, user: User):
        print("user.spotify_token_info", user.spotify_token_info)
        cache_handler = UserSpecificCacheHandler(user=user)
        settings = get_settings()
        spotify_oath = SpotifyOAuth(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
            redirect_uri=settings.spotify_redirect_uri,
            cache_handler=cache_handler,
        )
        super().__init__(oauth_manager=spotify_oath)
