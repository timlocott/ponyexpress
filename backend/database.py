import json
from datetime import date

from backend.entities import(
    UserInDB,
    UserCreate,
)

with open("backend/fake_db.json","r") as f:
    DB = json.load(f)

# users
    
def get_all_users() -> list[UserInDB]:
    """ 
    Get all users from the database 
    :return: list of users
    """

    return [UserInDB(**user_data) for user_data in DB["users"].values()]

def create_user(user_create: UserCreate) -> UserInDB:
    """
    Create new user in database
    :param user_create: attribute values for the new user
    :return: the new user
    """

    pass

# def get_user_by_id(u_id: str) -> UserInDB: 
#     """
#     Get user from database
#     :param u_id: id of the user
#     :return: the user
#     """

#     return UserInDB(**DB["users"][u_id])