from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from playola.config import Settings, get_settings
from playola.lib import users
from playola.models.tortoise import UserTrack
from playola.lib.errors import ItemNotFoundException
from playola.models.pydantic import UserTrack_Pydantic_List

router = APIRouter()


@router.get("/")
async def get_users():
    return await users.get_all_users()


@router.get("/{user_id}")
async def get_a_user(user_id: str):
    try:
        user = users.get_user(id=user_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@router.get("/{user_id}/userTracks")
async def get_user_tracks(user_id: str, settings: Settings = Depends(get_settings)):
    return await UserTrack_Pydantic_List.from_queryset(
        UserTrack.filter(user_id=user_id)
    )
    return await users.get_user_tracks(user_id=user_id)


@router.post("/{user_id}/refreshUserTracks")
async def refresh_user_tracks(
    user_id: str
):
    return await users.refresh_users_important_tracks(user_id=user_id)
