from sqlmodel import Session
from fastapi import APIRouter, Depends
from backend import database as db

from backend.entities import (
    ChatCollection,
    ChatResponse, 
    ChatUpdate,
    MessageCollection,
    UserCollection,
)

from backend.schema import (
    ChatInDB,
    UserChatLinkInDB,
)

chat_router = APIRouter(prefix="/chats", tags=["Chats"])

@chat_router.get("", response_model=ChatCollection)
def get_chats(session: Session = Depends(db.get_session)):
    """Get a collection of chats."""
    chats = db.get_all_chats(session)
    sort_key = lambda chat: getattr(chat, "name")
    return ChatCollection(
        meta={"count": len(chats)},
        chats=sorted(chats, key=sort_key)
    )

@chat_router.get("/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: str, session: Session = Depends(db.get_session)):
    """Gets a specific chat with the corresponding ID"""
    return db.get_chat_by_id(session, chat_id)

@chat_router.get("/{chat_id}/messages", response_model=MessageCollection)
def get_messages(chat_id: str, session: Session = Depends(db.get_session)):
    """Get a collection of messages for a specified chat."""
    messages = db.get_messages_by_chat_id(session, chat_id)
    sort_key = lambda message: getattr(message, "created_at")
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key)
    )

@chat_router.get("/{chat_id}/users", response_model=UserCollection)
def get_users(chat_id: str, session: Session = Depends(db.get_session)):
    """Get a collection of users for a specified chat."""
    users = db.get_users_by_chat_id(session, chat_id)
    sort_key = lambda user: getattr(user, "id")
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key)
    )

@chat_router.delete("/{chat_id}", response_model=None, status_code=204)
def delete_chat(chat_id: str, session: Session = Depends(db.get_session)):
    """Delete a chat"""
    db.delete_chat(session, chat_id)

@chat_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: str, chat_update: ChatUpdate, session: Session = Depends(db.get_session)):
    """Update a chat"""
    return db.update_chat_by_id(session, chat_id, chat_update)