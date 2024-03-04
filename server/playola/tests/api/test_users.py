from unittest.mock import AsyncMock
import pytest

from playola.models.tortoise import User


# HELP! Cannot get this to work -- (Can't seem to get a solid test-db/dev-db separation)
# The next thing I was going to try was to pull a db session using Depends in the router
# and pass it all the way down through all the inner functions, as referenced here:
#
#
@pytest.mark.asyncio
async def test_get_all_users(test_app_with_db):
    pass
    # user = (
    #     await User.create(
    #         spotify_token_info={
    #             "access_token": "THE ACCESS_TOKEN_1",
    #             "refresh_token": "THE_REFRESH_TOKEN_1",
    #         },
    #         spotify_user_id="the_spotify_user_id_1",
    #         spotify_display_name="the_display_name_1",
    #     ),
    # )

    # response = test_app_with_db.get("/api/v1/users")

    # assert response.status_code == 200
    # assert response.json().count == 1
