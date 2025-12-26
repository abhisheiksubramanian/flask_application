# -------------------------------------------------
# REGISTER USER – SUCCESS
# -------------------------------------------------
def test_register_user_success(client):
    res = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "pass123"}
    )
    assert res.status_code == 201
    assert res.json["message"] == "User registered"


# -------------------------------------------------
# REGISTER USER – DUPLICATE USER
# -------------------------------------------------
def test_register_user_duplicate(client):
    client.post(
        "/auth/register",
        json={"username": "testuser", "password": "pass123"}
    )

    res = client.post(
        "/auth/register",
        json={"username": "testuser", "password": "pass123"}
    )

    assert res.status_code == 400
    assert "error" in res.json


# -------------------------------------------------
# REGISTER USER – MISSING PASSWORD
# -------------------------------------------------
def test_register_user_missing_password(client):
    res = client.post(
        "/auth/register",
        json={"username": "testuser"}
    )

    assert res.status_code == 400
    assert res.json["error"] == "Username and password are required"


# -------------------------------------------------
# REGISTER USER – EMPTY JSON
# -------------------------------------------------
def test_register_user_empty_body(client):
    res = client.post(
        "/auth/register",
        json={}
    )

    assert res.status_code == 400
    assert res.json["error"] == "Username and password are required"


# -------------------------------------------------
# LOGIN USER – SUCCESS
# -------------------------------------------------
def test_login_user_success(client):
    client.post(
        "/auth/register",
        json={"username": "loginuser", "password": "pass123"}
    )

    res = client.post(
        "/auth/login",
        json={"username": "loginuser", "password": "pass123"}
    )

    assert res.status_code == 200
    assert "access_token" in res.json


# -------------------------------------------------
# LOGIN USER – WRONG PASSWORD
# -------------------------------------------------
def test_login_user_wrong_password(client):
    client.post(
        "/auth/register",
        json={"username": "loginuser", "password": "pass123"}
    )

    res = client.post(
        "/auth/login",
        json={"username": "loginuser", "password": "wrongpass"}
    )

    assert res.status_code == 401
    assert "error" in res.json


# -------------------------------------------------
# LOGIN USER – USER NOT FOUND
# -------------------------------------------------
def test_login_user_not_found(client):
    res = client.post(
        "/auth/login",
        json={"username": "nouser", "password": "pass123"}
    )

    assert res.status_code == 401
    assert "error" in res.json


# -------------------------------------------------
# LOGIN USER – MISSING PASSWORD
# -------------------------------------------------
def test_login_user_missing_password(client):
    res = client.post(
        "/auth/login",
        json={"username": "loginuser"}
    )

    assert res.status_code == 400
    assert res.json["error"] == "Username and password are required"


# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
def test_health_check(client):
    res = client.get("/auth/health")

    assert res.status_code == 200
    assert res.json["status"] == "UP"


from unittest.mock import patch
from app.exceptions.business import BusinessException


# -------------------------------------------------
# REGISTER USER – SERVICE EXCEPTION
# -------------------------------------------------
def test_register_user_business_exception(client):
    with patch(
        "app.controllers.auth_controller.register_user",
        side_effect=BusinessException("User already exists")
    ):
        res = client.post(
            "/auth/register",
            json={"username": "test", "password": "pass123"}
        )

        assert res.status_code == 400
        assert res.json["error"] == "User already exists"


# -------------------------------------------------
# LOGIN USER – SERVICE EXCEPTION
# -------------------------------------------------
def test_login_user_business_exception(client):
    with patch(
        "app.controllers.auth_controller.login_user",
        side_effect=BusinessException("Invalid credentials")
    ):
        res = client.post(
            "/auth/login",
            json={"username": "test", "password": "wrong"}
        )

        assert res.status_code == 401
        assert res.json["error"] == "Invalid credentials"
