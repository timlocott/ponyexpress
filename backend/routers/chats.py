from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends, Query
from backend import database as db

from backend.auth import get_current_user
from backend.entities import (
    ChatCollection,
    ChatResponse,
    ChatUpdate,
    Message,
    MessageCollection,
    MessageCreate,
    UserCollection,
)
from backend.schema import UserInDB

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

@chat_router.get("/{chat_id}")
def get_chat(chat_id: int, include: list = Query(None), session: Session = Depends(db.get_session)):
    """Gets a specific chat with the corresponding ID"""
    include_messages = False
    include_users = False
    if include:
        if "messages" in include:
            include_messages = True
        if "users" in include:
            include_users = True
    return db.get_chat_by_id(session, chat_id, include_messages, include_users)

@chat_router.get("/{chat_id}/messages", response_model=MessageCollection, status_code=201)
def get_messages(chat_id: int, session: Session = Depends(db.get_session)):
    """Get a collection of messages for a specified chat."""
    messages = db.get_messages_by_chat_id(session, chat_id)
    sort_key = lambda message: getattr(message, "created_at")
    return MessageCollection(
        meta={"count": len(messages)},
        messages=sorted(messages, key=sort_key)
    )

@chat_router.get("/{chat_id}/users", response_model=UserCollection)
def get_users(chat_id: int, session: Session = Depends(db.get_session)):
    """Get a collection of users for a specified chat."""
    users = db.get_users_by_chat_id(session, chat_id)
    sort_key = lambda user: getattr(user, "id")
    return UserCollection(
        meta={"count": len(users)},
        users=sorted(users, key=sort_key)
    )

# @chat_router.delete("/{chat_id}", response_model=None, status_code=204)
# def delete_chat(chat_id: str, session: Session = Depends(db.get_session)):
#     """Delete a chat"""
#     db.delete_chat(session, chat_id)

@chat_router.put("/{chat_id}", response_model=ChatResponse)
def update_chat(chat_id: int, 
                chat_update: ChatUpdate, 
                session: Session = Depends(db.get_session)):
    """Update a chat"""
    return db.update_chat_by_id(session=session, c_id=chat_id, chat_update=chat_update)

@chat_router.post("/{chat_id}/messages", response_model=Message)
def create_message_in_chat(chat_id: int,
                           message_create: MessageCreate, 
                           session: Session = Depends(db.get_session), 
                           user: UserInDB = Depends(get_current_user)):
    return db.create_message(session, chat_id, message_create, user)

