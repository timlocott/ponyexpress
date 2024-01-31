from fastapi.testclient import TestClient

from backend.main import app

def test_get_users():
    test_client = TestClient(app)
    response = test_client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_create_user():
    test_client = TestClient(app)
    response = test_client.post(
        "/users",
        json={"id":"test1"})
    assert response.status_code == 200
    assert response.json()["id"] == "test1"

    response = test_client.get(f"/users/{response.json()['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == "test1"

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
    id = "badID"
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

def test_get_user_by_id():
    id = "bishop"
    test_client = TestClient(app)
    response = test_client.get(f"/users/{id}")
    assert response.status_code == 200
    assert response.json()["id"] == "bishop"

