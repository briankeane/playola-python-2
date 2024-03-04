import datetime
from typing import Optional, List

from spotipy import oauth2, Spotify

from fastapi import Depends

from playola.lib.spotipy_extensions import UserSpecificSpotify
from playola.lib.errors import ItemNotFoundException
from playola.models.tortoise import User, Track, UserTrack
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


async def get_or_create_user_from_spotify_code(
    code: str, settings: Settings = Depends(get_settings)
) -> User:
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


async def get_all_users() -> List[User]:
    return await User.all()


async def refresh_users_important_tracks(user_id: str):
    user = await User.filter(id=user_id).first()
    if user is None:
        raise ItemNotFoundException

    sp = UserSpecificSpotify(user=user)
    track_infos_short_term = sp.current_user_top_tracks(
        limit=50, time_range="short_term"
    )["items"]
    track_infos_medium_term = sp.current_user_top_tracks(
        limit=50, time_range="medium_term"
    )["items"]
    track_infos_long_term = sp.current_user_top_tracks(
        limit=50, time_range="long_term"
    )["items"]

    all_track_infos = remove_duplicates(
        track_infos_short_term + track_infos_medium_term + track_infos_long_term
    )

    tracks = []

    for track_info in all_track_infos:
        (track, created) = await Track.get_or_create(
            spotify_id=track_info["id"],
            defaults={
                "album": parse_album(track_info),
                "artist": parse_artist(track_info),
                "duration_ms": track_info["duration_ms"],
                "isrc": parse_isrc(track_info),
                "title": track_info["name"],
                "popularity": track_info["popularity"],
                "spotify_image_link": parse_spotify_image_link(track_info),
            },
        )
        tracks.append(track)

    user_tracks = []
    for track in tracks:
        (track, created) = await UserTrack.get_or_create(
            user_id=user.id,
            track_id=track.id,
            status="new",
            defaults={"date_last_seen": datetime.datetime.now()},
        )
        await track.fetch_related("user", "track")
        user_tracks.append(track)

    return await UserTrack.filter(user_id=user_id).select_related("track")


def parse_album(track_info) -> str:
    return track_info["album"]["name"]


def parse_artist(track_info) -> Optional[str]:
    return track_info["artists"][0]["name"]


def parse_isrc(track_info) -> Optional[str]:
    return track_info.get("external_ids", {}).get("isrc", None)


def parse_spotify_image_link(track_info) -> Optional[str]:
    images = track_info["album"]["images"]
    if not len(images):
        return None
    return images[0]


def remove_duplicates(tracks_list: list):
    tracks_dict = {}
    final_list = []
    for track in tracks_list:
        if tracks_dict.get(track["id"]) is None:
            tracks_dict[track["id"]] = True
            final_list.append(track)
    return final_list


async def get_user(id):
    user = await User.filter(id=id).first()
    if user is None:
        raise ItemNotFoundException
    return user
