from app.main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    response = client.post("/users", json={"email": "emailfromtest@test.com"})
    assert response.status_code == 200
    response = response.json()
    assert isinstance(response["id"], int)
    assert response["email"] == "emailfromtest@test.com"
    assert response["profiles"] == []
    assert response["favorite_profiles"] == []
