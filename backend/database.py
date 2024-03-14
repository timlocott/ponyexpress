# import json
from sqlmodel import Session, SQLModel, create_engine, select
# from datetime import datetime

from backend.entities import(
    ChatNM,
    UserResponse,
    UserCreate,
    ChatUpdate,
    Message,
    ChatResponse,
)
from backend.schema import(
    UserChatLinkInDB,
    UserInDB,
    ChatInDB,
    MessageInDB,
)

engine = create_engine(
    "sqlite:///backend/pony_express.db",
    echo=True,
    connect_args={"check_same_thread": False},
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

# with open("backend/fake_db.json","r") as f:
#     DB = json.load(f)

#   ----------------------------- users ----------------------------- #
    
def get_all_users(session: Session) -> list[UserInDB]:
    """ 
    Get all users from the database 
    :return: list of users
    """
    return session.exec(select(UserInDB)).all()

def create_user(session: Session, user_create: UserCreate) -> UserResponse:
    """
    Create new user in database
    :param user_create: attribute values for the new user
    :return: the new user
    :raises: DuplicateChatException: If chat id is already exists
    """

    user = UserInDB(**user_create.model_dump())
    if user.id in get_all_users(session):
        raise DuplicateEntityException(entity_name="User", entity_id=user.id)
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserResponse(user=user)

def get_user_by_id(session: Session, u_id: int) -> UserResponse: 
    """
    Get user from database
    :param u_id: id of the user
    :return: the user
    :raises: EntityNotFoundException: If user id does not exist
    """
    user = session.get(UserInDB, u_id)
    if user:
        return UserResponse(user=user)
    raise EntityNotFoundException(entity_name="User", entity_id=u_id,)

def get_chats_by_user_id(session: Session, u_id: int) -> list[ChatNM]:
    """
    Get chats related to user id
    :param u_id: id of the user
    :return: list of chats
    :raises: EntityNotFoundException: If user id does not exist
    """
    user = get_user_by_id(session, u_id)
    # result : list[ChatNM] = []

    user = session.get(UserInDB, u_id)
    # for chat in user.chats:
    #     result.append(chat)

    # return result
    return user.chats

# ----------------------------- chats ----------------------------- #

def get_all_chats(session: Session) -> list[ChatInDB]:
    """
    Get all chats from the database
    :return: list of chats
    """
    return session.exec(select(ChatInDB)).all()

def get_chat_by_id(session: Session, c_id: int) -> ChatResponse: 
    """
    Get chat from database
    :param c_id: id of the chat
    :return: the chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = session.get(ChatInDB, c_id)
    if chat:
        return ChatResponse(chat=chat)
    raise EntityNotFoundException(entity_name="Chat", entity_id=c_id,)

def get_messages_by_chat_id(session: Session, c_id: int) -> list[Message]:
    """
    Get all messages for a specified chat
    :param c_id: id of the chat
    :return: list of messages
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat: ChatInDB = get_chat_by_id(session, c_id).chat
    return session.get(ChatInDB, c_id).messages

def get_users_by_chat_id(session: Session, c_id: int) -> list[UserInDB]:
    """
    Get all users for a specified chat
    :param c_id: id of the chat
    :return: list of users
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat: ChatInDB = get_chat_by_id(session, c_id).chat
    return session.get(ChatInDB, c_id).users

def delete_chat(session: Session, c_id: int) -> None:
    """
    Delete chat from database
    :param c_id: id of the chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = get_chat_by_id(session, c_id).chat
    session.delete(chat)
    session.commit()

def update_chat_by_id(session: Session, c_id: int, chat_update: ChatUpdate) -> ChatResponse:
    """
    Update chat
    :param c_id: id of chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = get_chat_by_id(session, c_id).chat
    
    for attr, value in chat_update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, value)

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return ChatResponse(chat=chat)

# ----------------------------- exception classes ----------------------------- #

class EntityNotFoundException(Exception):
    def __init__ (self, *, entity_id: int, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__ (self, *, entity_id: int, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id