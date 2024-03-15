from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int
class ChatMetadata(BaseModel):
    """Represents metadata for a chat."""
    message_count: int
    user_count: int

# ----------------------------- messages ----------------------------- #

class Message(SQLModel):
    """Data model for message."""
    id: int
    text: str
    chat_id: int
    user: "User"
    created_at: datetime

class MessageCreate(SQLModel):
    text: str = None

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
    created_at: datetime

class UserCreate(SQLModel):
    """Represents model for adding a new user to the system."""
    username: str
    email: str
    hashed_password: str

class UserUpdate(SQLModel):
    """Represents a request model for updating a user"""
    username: str = None
    email: str = None

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
    owner: User
    created_at: datetime
    messages: list[Message]

class ChatNM(SQLModel):
    """Represents an API response for a chat without messages"""
    id: int
    name: str
    owner: User
    created_at: datetime

class ChatUpdate(SQLModel):
    """Represents a request model for updating a chat"""
    id: int = None
    name: str = None
    owner: User = None
    messages: list[Message] = None
    created_at: datetime = None

class ChatCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    chats: list[ChatNM]

class ChatResponse(BaseModel):
    """Represents an API response for a chat."""
    meta: ChatMetadata
    chat: ChatNM

class ChatResponseMessages(ChatResponse):
    """Represents an API response for a chat that includes messages"""
    messages: list[Message]

class ChatResponseUsers(ChatResponse):
    """Represents an API response for a chat that includes users"""
    users: list[User]

class ChatResponseMessageAndUsers(ChatResponse):
    """Represents an API response for a chat that includes messages and users"""
    messages: list[Message]
    users: list[User]