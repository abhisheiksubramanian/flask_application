from app.tests.utils import register_and_login
from app.extensions.db import db
from app.models.user import User


def make_admin(client):
    token = register_and_login(client, "admin", "admin123")

    # make user ADMIN directly in DB
    user = User.query.filter_by(username="admin").first()
    user.role = "ADMIN"
    db.session.commit()

    return token


# -------------------------------
# CREATE ORDER (USER)
# -------------------------------
def test_create_order(client):
    token = register_and_login(client, "user1", "pass123")

    res = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={"total_amount": 500}
    )

    assert res.status_code == 201
    assert "id" in res.json


# -------------------------------
# GET ORDER BY ID (USER)
# -------------------------------
def test_get_order_by_id(client):
    token = register_and_login(client, "user1", "pass123")

    create = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={"total_amount": 700}
    )

    order_id = create.json["id"]

    res = client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert res.json["amount"] == 700.0


# -------------------------------
# LIST ORDERS (USER)
# -------------------------------
def test_list_orders_user(client):
    token = register_and_login(client, "user1", "pass123")

    client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={"total_amount": 300}
    )

    res = client.get(
        "/orders",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200
    assert isinstance(res.json, list)


# -------------------------------
# DELETE ORDER (USER)
# -------------------------------
def test_delete_order(client):
    token = register_and_login(client, "user1", "pass123")

    create = client.post(
        "/orders",
        headers={"Authorization": f"Bearer {token}"},
        json={"total_amount": 400}
    )

    order_id = create.json["id"]

    res = client.delete(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200


# -------------------------------
# ADMIN – LIST ALL ORDERS (PAGINATED)
# -------------------------------
def test_admin_list_orders_paginated(client):
    admin_token = make_admin(client)

    # create few orders
    client.post(
        "/orders",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"total_amount": 100}
    )

    res = client.get(
        "/orders/admin/all?page=1&size=5",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert res.status_code == 200
    assert "data" in res.json
    assert "total_records" in res.json


def make_admin(client):
    # 1️⃣ Register user
    client.post(
        "/auth/register",
        json={"username": "admin", "password": "admin123"}
    )

    # 2️⃣ Update role BEFORE login
    user = User.query.filter_by(username="admin").first()
    user.role = "ADMIN"
    db.session.commit()

    # 3️⃣ Login AFTER role update
    login = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )

    return login.json["access_token"]

