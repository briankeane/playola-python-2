from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from playola.models.tortoise import UserTrack


class UserSchema(BaseModel):
    spotify_user_id: str
    display_name: str


class SpotifyCodePayloadSchema(BaseModel):
    code: str


UserTrack_Pydantic = pydantic_model_creator(UserTrack)
UserTrack_Pydantic_List = pydantic_queryset_creator(UserTrack)
