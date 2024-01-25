from fastapi import APIRouter, HTTPException
from backend import database as db

from backend.entities import (
    UserCollection,
    # UserCreate,
    # UserInDB,
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

@user_router.post("/users",
          description="Creates a new user",
          name="Create user")
def create_user():
    pass

@user_router.get("/users/{user_id}",
         description="Returns a user for a given id",
         name="Get User")
def get_user():
    pass
