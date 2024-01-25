from datetime import datetime

from pydantic import BaseModel

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

class Metadata(BaseModel):
    """Represents metadata for a collection."""
    count: int

class UserCollection(BaseModel):
    """Represents an API response for a collection of users."""
    meta: Metadata
    users: list[UserInDB]