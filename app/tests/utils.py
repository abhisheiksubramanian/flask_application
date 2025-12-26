def register_and_login(client, username, password):
    client.post(
        "/auth/register",
        json={"username": username, "password": password}
    )

    login = client.post(
        "/auth/login",
        json={"username": username, "password": password}
    )

    return login.json["access_token"]
