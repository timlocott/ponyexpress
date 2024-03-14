from fastapi.testclient import TestClient
from backend.main import app

# ----------------------------- users ----------------------------- #

def test_get_users(session, client, default_users):
    session.add_all(default_users)
    session.commit()
    expected_usernames = ["timlocott", "lizzybobizzy", "capone1"]

    response =  client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])
    assert [user["username"] for user in users] == expected_usernames

def test_create_user():
    test_client = TestClient(app)
    response = test_client.post(
        "/users",
        json={"id":"test1"})
    assert response.status_code == 200
    assert response.json()["user"]["id"] == "test1"

    response = test_client.get(f"/users/{response.json()['user']['id']}")
    response = test_client.get(f"/users/test1")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == "test1"

def test_create_user_with_dup_id():
    id = "bishop"
    test_client = TestClient(app)
    response = test_client.post(
        "/users",
        json={"id": id})
    assert response.status_code == 422
    assert response.json() == {
        "detail": {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": id,
        }
    }

def test_get_user_by_invalid_id():
    id = 900
    test_client = TestClient(app)
    response = test_client.get(f"/users/{id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": id,
        }
    }

def test_get_user_by_id(session, client, default_users):
    session.add_all(default_users)
    session.commit()
    id = 1
    response = client.get(f"/users/{id}")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == 1
    assert response.json()["user"]["username"] == "timlocott"

# ----------------------------- chats ----------------------------- #
    
def test_get_chats(session, client, default_users, default_chats):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.commit()
    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda user: user["name"])

def test_get_chat_by_invalid_id():
    id = 900
    test_client = TestClient(app)
    response = test_client.get(f"/chats/{id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": id,
        }
    }

def test_get_chat_by_id(session, client, default_users, default_chats):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.commit()

    id = 3
    response = client.get(f"/chats/{id}")
    assert response.status_code == 200
    assert response.json()["chat"]["name"] == "Cool Group Chat"

def test_get_messages_by_vaild_id(session, client, default_users, default_chats, default_messages):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.add_all(default_messages)
    session.commit()

    id = 3
    response = client.get(f"/chats/{id}/messages")
    assert response.status_code == 200

    meta = response.json()["meta"]
    messages = response.json()["messages"]
    assert meta["count"] == len(messages)
    assert messages == sorted(messages, key=lambda message: message["created_at"])

def test_get_messages_by_invalid_id():
    id = 900
    test_client = TestClient(app)
    response = test_client.get(f"/chats/{id}/messages")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": id,
        }
    }

def test_get_users_by_vaild_id(session, client, default_users, default_chats, default_messages):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.add_all(default_messages)
    session.commit()

    id = 3
    response = client.get(f"/chats/{id}/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda message: message["id"])

def test_get_users_by_invalid_id():
    id = 900
    test_client = TestClient(app)
    response = test_client.get(f"/chats/{id}/users")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": id,
        }
    }

def test_delete_chat_valid_id():
    id = 3
    test_client = TestClient(app)
    response = test_client.delete(f"/chats/{id}")
    assert response.status_code == 204

    response = test_client.get(f"/chats/{id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": id,
        }
    }

def test_delete_chat_invalid_id():
    id = 900
    test_client = TestClient(app)
    response = test_client.delete(f"/chats/{id}")
    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": id,
        }
    }

def test_update_chat_valid_id(session, client, default_users, default_chats):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.commit()

    id = 3
    update_params = { "name": "test test test"}
    response = client.put(f"/chats/{id}", json=update_params)

    assert response.status_code == 200
    chat = response.json()["chat"]
    for key, value in update_params.items():
        assert chat[key] == value

    response = client.get(f"/chats/{id}")
    assert response.status_code == 200
    chat = response.json()["chat"]
    # assert chat.name == update_params["name"]
    for key, value in update_params.items():
        assert chat[key] == value

def test_update_chat_invalid_id():
    id = 900
    update_params = { "name": "test test test"}
    test_client = TestClient(app)
    response = test_client.put(f"/chats/{id}", json=update_params)

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": id,
        }
    }

def test_get_chats_by_valid_user_id(session, client, default_users, default_chats):
    session.add_all(default_users)
    session.add_all(default_chats)
    session.commit()

    id = 1
    response = client.get(f"/users/{id}/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda message: message["name"])

def test_get_chats_by_invalid_user_id():
    id = 900
    test_client = TestClient(app)
    response = test_client.get(f"/users/{id}/chats")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": id,
        }
    }






