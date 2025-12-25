from flask_jwt_extended import create_access_token

def admin_token(client):
    client.post(
        "/auth/register",
        json={"username": "admin", "password": "admin123"}
    )

    login = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )

    return login.json["access_token"]
