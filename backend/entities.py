from datetime import datetime

from pydantic import BaseModel

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

# ----------------------------- messages ----------------------------- #

class Message(BaseModel):
    """Represents an API response for a message."""
    id: str
    user_id: str
    text: str
    created_at: datetime

class MessageCollection(BaseModel):
    """Represents an API response for a collection of messages."""
    meta: Metadata
    messages: list[Message]

# ----------------------------- users ----------------------------- #
    
class User(BaseModel):
    """Represents an API response for a user."""
    id: str
    created_at: datetime

class UserInDB(BaseModel):
    """Represents a user in the database."""
    id: str
    created_at: datetime

class UserCreate(BaseModel):
    """Represents parameters for adding a new user to the system."""
    id: str

class UserResponse(BaseModel):
    user: UserInDB

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    users: list[UserInDB]

# ----------------------------- chats ----------------------------- #
    
class Chat(BaseModel):
    """Represents an API response for a chat."""
    id: str
    name: str
    user_ids: list[str]
    messages: list[Message]
    owner_id: str
    created_at: datetime

class ChatNM(BaseModel):
    """Represents an API response for a chat."""
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime

class ChatInDB(BaseModel):
    """Represents a chat in the database."""
    id: str
    name: str
    user_ids: list[str]
    messages: list[Message]
    owner_id: str
    created_at: datetime

class ChatUpdate(BaseModel):
    id: str = None
    name: str = None
    user_ids: list[str] = None
    messages: list[Message] = None
    owner_id: str = None
    created_at: datetime = None

class ChatCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    chats: list[ChatNM]

class ChatResponse(BaseModel):
    chat: ChatNM