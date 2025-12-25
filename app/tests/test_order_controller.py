
from app.tests.utils import admin_token


def test_create_order(client, user_token):
    response = client.post(
        "/orders",
        json={"total_amount": 1500},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 201
    assert "id" in response.json


def test_list_orders(client, user_token):
    client.post(
        "/orders",
        json={"total_amount": 1000},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    response = client.get(
        "/orders",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_order_by_id(client, user_token):
    create_resp = client.post(
        "/orders",
        json={"total_amount": 2000},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    order_id = create_resp.json["id"]

    response = client.get(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200
    assert response.json["id"] == order_id


def test_delete_order(client, user_token):
    create_resp = client.post(
        "/orders",
        json={"total_amount": 500},
        headers={"Authorization": f"Bearer {user_token}"}
    )

    order_id = create_resp.json["id"]

    response = client.delete(
        f"/orders/{order_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 200


def test_admin_orders_access_denied(client, user_token):
    response = client.get(
        "/orders/admin/all",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code == 403


def test_admin_orders_success(client, admin_token):
    response = client.get(
        "/orders/admin/all",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    assert response.status_code == 200

def test_admin_orders_paginated(client):
    token = admin_token(client)

    response = client.get(
        "/orders/admin/all?page=1&size=5",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in (200, 404)
    if response.status_code == 200:
        assert "page" in response.json
        assert "size" in response.json
        assert "data" in response.json