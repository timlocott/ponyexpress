# import json
from sqlmodel import Session, SQLModel, create_engine, select
# from datetime import datetime

from backend.entities import(
    ChatMetadata,
    ChatNM,
    ChatResponseChat,
    ChatResponseMessageAndUsers,
    ChatResponseMessages,
    ChatResponseUsers,
    MessageCreate,
    MessageResponse,
    UserResponse,
    UserCreate,
    ChatUpdate,
    Message,
    ChatResponse,
    UserUpdate,
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
    :param session: session
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

def update_user_by_id(session: Session, u_id: int, user_update: UserUpdate) -> UserResponse:
    """
    Update user
    :param u_id: id of user
    :param user_update: user update request model
    :param session: session
    """

    user = session.get(UserInDB, u_id)
    
    for attr, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, attr, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return UserResponse(user=user)

def get_user_by_id(session: Session, u_id: int) -> UserResponse: 
    """
    Get user from database
    :param session: session
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
    :param session: session
    :param u_id: id of the user
    :return: list of chats
    :raises: EntityNotFoundException: If user id does not exist
    """
    get_user_by_id(session, u_id)
    user = session.get(UserInDB, u_id)

    return user.chats

# ----------------------------- chats ----------------------------- #

def get_all_chats(session: Session) -> list[ChatInDB]:
    """
    Get all chats from the database
    :return: list of chats
    """
    return session.exec(select(ChatInDB)).all()

def get_chat_by_id(session: Session, c_id: int, include_messages: bool, include_users: bool): 
    """
    Get chat from database
    :param session: session
    :param c_id: id of the chat
    :return: the chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = session.get(ChatInDB, c_id)
    if chat:
        meta = ChatMetadata(
            message_count=len(chat.messages),
            user_count=len(chat.users)
        )
        if include_messages and not include_users:
            return ChatResponseMessages(
                meta=meta,
                chat=chat,
                messages=chat.messages
            )
        elif not include_messages and include_users:
            return ChatResponseUsers(
                meta=meta,
                chat=chat,
                users=chat.users
            )
        elif include_messages and include_users:
            return ChatResponseMessageAndUsers(
                meta=meta,
                chat=chat,
                messages=chat.messages,
                users=chat.users
            )
        else:
            return ChatResponse(
                meta= meta,
                chat=chat,
            )
        #________________________________________________________________#
        # meta=ChatMetadata(
        #     message_count=len(chat.messages),
        #     user_count=len(chat.users)
        # ),
        # include_data = {
        #     "meta": meta,
        #     "chat": chat,
        # }
        # if include_messages:
        #     include_data["messages"] = chat.messages
        # if include_users:
        #     include_data["users"] = chat.users
        # # return ChatResponse(
        # #     meta=ChatMetadata(
        # #         message_count=len(chat.messages),
        # #         user_count=len(chat.users)
        # #     ),
        # #     chat=chat,
        # #     messages = chat.messages if include_messages else None,
        # #     users = chat.users if include_users else None
        # # )
        # print(include_data)
        # return ChatResponse(**include_data)
    raise EntityNotFoundException(entity_name="Chat", entity_id=c_id,)

def create_message(session: Session, chat_id: int, message_create: MessageCreate, user: UserInDB) -> MessageResponse:
    """
    Create new message in database
    :param session: session
    :param message_create: message create request model
    :param user: user owning message
    :return: the new message
    """
    get_chat_by_id(session, chat_id, False, False)
    message = MessageInDB(
        **message_create.model_dump(),
        chat_id=chat_id,
        user=user
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return MessageResponse(message=message)

def get_messages_by_chat_id(session: Session, c_id: int) -> list[Message]:
    """
    Get all messages for a specified chat
    :param session: session
    :param c_id: id of the chat
    :return: list of messages
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat: ChatInDB = get_chat_by_id(session, c_id, False, False).chat
    return session.get(ChatInDB, c_id).messages

def get_users_by_chat_id(session: Session, c_id: int) -> list[UserInDB]:
    """
    Get all users for a specified chat
    :param session: session
    :param c_id: id of the chat
    :return: list of users
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat: ChatInDB = get_chat_by_id(session, c_id, False, False).chat
    return session.get(ChatInDB, c_id).users

def delete_chat(session: Session, c_id: int) -> None:
    """
    Delete chat from database
    :param session: session
    :param c_id: id of the chat
    :raises: EntityNotFoundException: If chat id does not exist
    """
    chat = get_chat_by_id(session, c_id, False, False).chat
    session.delete(chat)
    session.commit()

def update_chat_by_id(session: Session, c_id: int, chat_update: ChatUpdate) -> ChatResponseChat:
    """
    Update chat
    :param session: session
    :param c_id: id of chat
    :param chat_update: chat update request model
    :raises: EntityNotFoundException: If chat id does not exist
    """
    get_chat_by_id(session, c_id, False, False)
    chat = session.get(ChatInDB, c_id)
    
    for attr, value in chat_update.model_dump(exclude_unset=True).items():
        setattr(chat, attr, value)

    session.add(chat)
    session.commit()
    session.refresh(chat)
    
    return ChatResponseChat(chat=chat)

# ----------------------------- exception classes ----------------------------- #

class EntityNotFoundException(Exception):
    def __init__ (self, *, entity_id: int, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id

class DuplicateEntityException(Exception):
    def __init__ (self, *, entity_id: int, entity_name: str):
        self.entity_name = entity_name
        self.entity_id = entity_id