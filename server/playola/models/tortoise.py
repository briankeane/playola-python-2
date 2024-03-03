# project/app/models/tortoise.py


from tortoise import fields, models


class SpotifyUser(models.Model):
    token_info = fields.JSONField()
    spotify_user_id = fields.CharField(max_length=512)
    display_name = fields.CharField(max_length=512)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} -- {self.spotify_user_id}"
