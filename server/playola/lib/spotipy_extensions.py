from playola.config import get_settings
from playola.models.tortoise import Curator
from spotipy import CacheHandler, Spotify, SpotifyOAuth


class UserSpecificCacheHandler(CacheHandler):
    def __init__(self, curator):
        self.curator = curator

    def get_cached_token(self):
        print("getting cached info", self.curator.spotify_token_info)
        return self.curator.spotify_token_info

    def save_token_to_cache(self, token_info):
        print("saving token info: ", token_info)
        self.curator.spotify_token_info = token_info
        self.curator.save()


class UserSpecificSpotify(Spotify):
    def __init__(self, curator: Curator):
        print("curator.spotify_token_info", curator.spotify_token_info)
        cache_handler = UserSpecificCacheHandler(curator=curator)
        settings = get_settings()
        spotify_oath = SpotifyOAuth(
            client_id=settings.spotify_client_id,
            client_secret=settings.spotify_client_secret,
            redirect_uri=settings.spotify_redirect_uri,
            cache_handler=cache_handler,
        )
        super().__init__(oauth_manager=spotify_oath)
