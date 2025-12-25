
def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json["message"] == "User registered"


def test_register_duplicate_user(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })

    response = client.post("/auth/register", json={
        "username": "testuser",
        "password": "password123"
    })

    assert response.status_code == 400


def test_login_success(client):
    client.post("/auth/register", json={
        "username": "loginuser",
        "password": "password123"
    })

    response = client.post("/auth/login", json={
        "username": "loginuser",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "username": "wrong",
        "password": "wrong"
    })

    assert response.status_code == 401


def test_health_endpoint(client):
    response = client.get("/auth/health")
    assert response.status_code == 200
    assert response.json["status"] == "UP"
