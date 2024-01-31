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
    user = UserInDB(
        created_at=date.today(),
        **user_create.model_dump(),
    )

    if user.id in DB["users"]:
        raise DuplicateEntityException(entity_name="User", entity_id=user.id)
    DB["users"][user.id] = user.model_dump()
    return user

def get_user_by_id(u_id: str) -> UserInDB: 
    """
    Get user from database
    :param u_id: id of the user
    :return: the user
    :raises: EntityNotFoundException: If user id does not exist
    """
    if u_id in DB["users"]:
        return UserInDB(**DB["users"][u_id])
    raise EntityNotFoundException(entity_name="User", entity_id=u_id,)

class EntityNotFoundException(Exception):
    def __init__ (self, *, entity_id: str, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__ (self, *, entity_id: str, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id