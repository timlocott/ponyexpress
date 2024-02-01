import json
from datetime import datetime

from backend.entities import(
    ChatNM,
    UserResponse,
    UserInDB,
    UserCreate,
    ChatInDB,
    ChatUpdate,
    Message,
    ChatResponse,
)

with open("backend/fake_db.json","r") as f:
    DB = json.load(f)

#   ----------------------------- users ----------------------------- #
    
def get_all_users() -> list[UserInDB]:
    """ 
    Get all users from the database 
    :return: list of users
    """
    return [UserInDB(**user_data) for user_data in DB["users"].values()]

def create_user(user_create: UserCreate) -> UserResponse:
    """
    Create new user in database
    :param user_create: attribute values for the new user
    :return: the new user
    :raises: DuplicateChatException: If chat id is already exists
    """
    user = UserInDB(
        created_at=datetime.now(), 
        **user_create.model_dump(),
    )

    if user.id in DB["users"]:
        raise DuplicateEntityException(entity_name="User", entity_id=user.id)
    DB["users"][user.id] = user.model_dump()
    return UserResponse(user=user)

def get_user_by_id(u_id: str) -> UserResponse: 
    """
    Get user from database
    :param u_id: id of the user
    :return: the user
    :raises: EntityNotFoundException: If user id does not exist
    """
    if u_id in DB["users"]:
        return UserResponse(user=UserInDB(**DB["users"][u_id]))
    raise EntityNotFoundException(entity_name="User", entity_id=u_id,)

def get_chats_by_user_id(u_id: str) -> list[ChatNM]:
    """
    Get chats related to user id
    :param u_id: id of the user
    :return: list of chats
    :raises: EntityNotFoundException: If user id does not exist
    """
    user = get_user_by_id(u_id)
    result : list[ChatNM] = []
    chats = get_all_chats()
    for chat in chats:
        for id in chat.user_ids:
            print("u_ids:" + id)
            if id == u_id:
                result.append(chat)

    return result

# ----------------------------- chats ----------------------------- #

def get_all_chats() -> list[ChatNM]:
    """
    Get all chats from the database
    :return: list of chats
    """
    return [ChatNM(**chat_data) for chat_data in DB["chats"].values()]

def get_chat_by_id(c_id: str) -> ChatResponse: 
    """
    Get chat from database
    :param c_id: id of the chat
    :return: the chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    if c_id in DB["chats"]:
        return ChatResponse(chat=ChatNM(**DB["chats"][c_id]))
    raise EntityNotFoundException(entity_name="Chat", entity_id=c_id,)

def get_messages_by_chat_id(c_id: str) -> list[Message]:
    """
    Get all messages for a specified chat
    :param c_id: id of the chat
    :return: list of messages
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat: ChatInDB = get_chat_by_id(c_id).chat
    return [Message(**message_data) for message_data in DB["chats"][chat.id]["messages"]]

def get_users_by_chat_id(c_id: str) -> list[UserInDB]:
    """
    Get all users for a specified chat
    :param c_id: id of the chat
    :return: list of users
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat: ChatInDB = get_chat_by_id(c_id).chat
    users = [get_user_by_id(user_data).user for user_data in DB["chats"][chat.id]["user_ids"]]
    return users

def delete_chat(c_id: str) -> None:
    """
    Delete chat from database
    :param c_id: id of the chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = get_chat_by_id(c_id).chat
    del DB["chats"][chat.id]

def update_chat_by_id(c_id: str, chat_update: ChatUpdate) -> ChatResponse:
    """
    Update chat
    :param c_id: id of chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = get_chat_by_id(c_id).chat
    
    for attr, value in chat_update.model_dump(exclude_none=True).items():
        setattr(chat, attr, value)

    DB["chats"][chat.id] = chat.model_dump()

    return ChatResponse(chat=chat)

# ----------------------------- exception classes ----------------------------- #

class EntityNotFoundException(Exception):
    def __init__ (self, *, entity_id: str, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__ (self, *, entity_id: str, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id