from pydantic import BaseModel

class UserSchema(BaseModel):
  spotify_user_id: str
  display_name: str

class SpotifyCodePayloadSchema(BaseModel):
  code: str
