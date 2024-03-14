import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine
from datetime import datetime

from backend.main import app
from backend import database as db
from backend.schema import (
    UserInDB,
    ChatInDB,
    MessageInDB,
)


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session):
    def _get_session_override():
        return session

    app.dependency_overrides[db.get_session] = _get_session_override

    yield TestClient(app)

    app.dependency_overrides.clear()

@pytest.fixture
def default_users():
    return [
        UserInDB(
            id=1,
            username="timlocott",
            email="timlocott@cool.email",
            hashed_password="1234567",
            created_at=datetime.fromisoformat("2024-05-05"),
        ),
        UserInDB(
            id=2,
            username="lizzybobizzy",
            email="lizzybobizzy@cool.email",
            hashed_password="1234567",
            created_at=datetime.fromisoformat("2023-05-05"),
        ),
        UserInDB(
            id=3,
            username="capone1",
            email="capone1@cool.email",
            hashed_password="1234567",
            created_at=datetime.fromisoformat("2022-05-05"),
        ),
    ]

@pytest.fixture
def default_chats():
    return [
        ChatInDB(
            id=1,
            name="Dear John",
            owner_id=1,
            created_at=datetime.fromisoformat("2024-05-05"),
        ),
        ChatInDB(
            id=2,
            name="Mailbox",
            owner_id=2,
            created_at=datetime.fromisoformat("2023-05-05"),
        ),
        ChatInDB(
            id=3,
            name="Cool Group Chat",
            owner_id=3,
            created_at=datetime.fromisoformat("2022-05-05"),
        ),
    ]

@pytest.fixture
def default_messages():
    return [
        MessageInDB(
            id= 1,
            text= "Hey John",
            user_id= 2,
            chat_id= 1,
            created_at= datetime.fromisoformat("2022-05-05"),
        ),
        MessageInDB(
            id= 2,
            text= "See ya",
            user_id= 2,
            chat_id= 1,
            created_at= datetime.fromisoformat("2022-05-05"),
        ),
        MessageInDB(
            id= 3,
            text= "Wait what?",
            user_id= 1,
            chat_id= 1,
            created_at= datetime.fromisoformat("2022-05-05"),
        ),
        MessageInDB(
            id= 4,
            text= "Hey want a job?",
            user_id= 3,
            chat_id= 2,
            created_at= datetime.fromisoformat("2022-05-05"),
        ),
        MessageInDB(
            id= 5,
            text= "No thanks",
            user_id= 1,
            chat_id= 2,
            created_at= datetime.fromisoformat("2022-05-05"),
        ),
        MessageInDB(
            id= 6,
            text= "Duuuuude",
            user_id= 1,
            chat_id= 3,
            created_at= datetime.fromisoformat("2022-05-05"),
        ),
    ]