import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client

def test_get_users(test_client):
    response = test_client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user(test_client):
    response = test_client.post("/users", json={"email": "emailfromtest@test.com"})
    assert response.status_code == 200
    response = response.json()
    assert isinstance(response["id"], int)
    assert response["email"] == "emailfromtest@test.com"
    assert response["profiles"] == []
    assert response["favorite_profiles"] == []
