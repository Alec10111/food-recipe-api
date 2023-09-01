from src.tests.conftest import *

client = TestClient(app)


def test_create_user():
    response = client.post("/users", json=SAMPLE_USER)
    assert response.status_code == 201


def test_create_user_existing_email(user):
    SAMPLE_USER["email"] = user["email"]
    response = client.post("/users", json=SAMPLE_USER)
    assert response.status_code == 400


def test_retrieve_different_user_unauthorized(user):
    response = client.get(f"/users/{user['_id']}")
    assert response.status_code == 401


def test_retrieve_different_user(user, user_auth):
    _, token = user_auth
    response = client.get(f"/users/{user['_id']}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_retrieve_my_user_unauthorized():
    response = client.get(f"/me")
    assert response.status_code == 401


def test_retrieve_my_user(user_auth):
    _, token = user_auth
    response = client.get(f"/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_list_users_unauthorized():
    response = client.get(f"/users")
    assert response.status_code == 401


def test_list_users(user_auth):
    _, token = user_auth
    response = client.get(f"/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 1
