import os


TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["playola.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}
