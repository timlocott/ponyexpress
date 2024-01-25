from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

chat_router = APIRouter(prefix="/chats", tags=["Chats"])

class Chat(BaseModel):
    id: str
    name: str
    user_ids: list[str]
    owner_id: str
    created_at: datetime