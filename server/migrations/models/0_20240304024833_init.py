from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "track" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "spotify_id" VARCHAR(512) NOT NULL UNIQUE,
    "album" VARCHAR(512) NOT NULL,
    "artist" VARCHAR(512) NOT NULL,
    "duration_ms" INT NOT NULL,
    "isrc" VARCHAR(512) NOT NULL,
    "title" VARCHAR(512) NOT NULL,
    "popularity" INT NOT NULL,
    "spotify_image_link" VARCHAR(512) NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "spotify_token_info" JSONB NOT NULL,
    "spotify_user_id" VARCHAR(512) NOT NULL,
    "spotify_display_name" VARCHAR(512) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "usertrack" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" VARCHAR(512) NOT NULL,
    "track_id" INT NOT NULL REFERENCES "track" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
