from fastapi import APIRouter
from backend import database as db

from backend.entities import (
    ChatCollection,
    UserCollection,
    UserCreate,
    UserInDB,
    UserResponse,
)

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("", response_model=UserCollection)
def get_users():
    """Get a collection of users."""
    users = db.get_all_users()
    sort_key = lambda user: getattr(user, "id")
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key)
    )

@user_router.post("", response_model=UserResponse)
def create_user(user_create: UserCreate):
    """Create a user"""
    return db.create_user(user_create)

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Gets a specific user with the corresponding ID"""
    return db.get_user_by_id(user_id)

@user_router.get("/{user_id}/chats", response_model=ChatCollection)
def get_chats(user_id: str):
    """Gets collection of chats related to user"""
    chats = db.get_chats_by_user_id(user_id)
    sort_key = lambda chat: getattr(chat, "name")
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key)
    )