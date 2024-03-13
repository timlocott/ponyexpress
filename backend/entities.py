from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

# ----------------------------- messages ----------------------------- #

class Message(SQLModel):
    """Data model for message."""
    id: int
    text: str
    user_id: int
    chat_id: int
    created_at: datetime

class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""
    meta: Metadata
    messages: list[Message]

# ----------------------------- users ----------------------------- #
    
class User(SQLModel):
    """Data model for user."""
    id: int
    username: str
    email: str
    hashed_password: str
    created_at: datetime
# class UserInDB(BaseModel):
#     """Represents a user in the database."""
#     id: str
#     created_at: datetime

class UserCreate(SQLModel):
    """Represents model for adding a new user to the system."""
    id: int
    username: str
    email: str
    hashed_password: str

class UserResponse(BaseModel):
    """Represents an API response for a user."""
    user: User

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    users: list[User]

# ----------------------------- chats ----------------------------- #
    
class Chat(SQLModel):
    """Data model for a chat."""
    id: int
    name: str
    owner_id: int
    created_at: datetime
    user_ids: list[int]
    messages: list[Message]

class ChatNM(SQLModel):
    """Represents an API response for a chat without messages"""
    id: int
    name: str
    owner_id: int
    user_ids: list[int]
    created_at: datetime

# class ChatInDB(BaseModel):
#     """Represents a chat in the database."""
#     id: str
#     name: str
#     user_ids: list[str]
#     messages: list[Message]
#     owner_id: str
#     created_at: datetime

class ChatUpdate(SQLModel):
    id: int = None
    name: str = None
    owner_id: int = None
    user_ids: list[int] = None
    messages: list[Message] = None
    created_at: datetime = None

class ChatCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    chats: list[ChatNM]

class ChatResponse(BaseModel):
    """Represents an API response for a chat."""
    chat: ChatNM