"""
=========================================================
ORDER CONTROLLER – ORDER SERVICE
=========================================================

This file contains all Order-related APIs.

📌 What this controller provides:
--------------------------------
1. Create a new order (USER)
2. Get order by ID (USER)
3. List user orders (USER)
4. Delete order (USER)
5. List all orders (ADMIN only)

📌 Security:
------------
- JWT authentication is required for all APIs
- ADMIN-only API is protected using role-based decorator

📌 Swagger Documentation:
-------------------------
- Swagger UI reads the YAML written inside docstrings
- `parameters: in: body` is used for request input
- This ensures input fields are visible in Swagger UI

📌 Swagger URL:
---------------
http://127.0.0.1:5000/apidocs/

=========================================================
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity

from app.services.order_service import (
    create_order,
    get_order,
    list_orders,
    delete_order,
    list_orders_paginated
)
from app.security.decorators import role_required
from app.security.roles import ROLE_ADMIN

# -------------------------------------------------
# Blueprint definition
# -------------------------------------------------
order_bp = Blueprint("orders", __name__)

        
# -------------------------------------------------
# CREATE ORDER (USER)
# -------------------------------------------------
@order_bp.route("", methods=["POST"])
@jwt_required()
def create():
    """
    Create Order
    ---
    tags:
      - Orders
    description: |
      This API creates a new order for the logged-in user.

      🔹 Flow:
      1. JWT token is validated
      2. User ID is extracted from token
      3. Order is created in database

      🔹 Beginner Notes:
      - User identity comes from JWT, not request body
      - Business logic is handled in service layer

    parameters:
      - in: body
        name: body
        required: true
        description: Order creation payload
        schema:
          type: object
          required:
            - total_amount
          properties:
            total_amount:
              type: number
              example: 1200.50

    responses:
      201:
        description: Order created successfully
      401:
        description: Unauthorized (JWT missing or invalid)
    """

    user_id = int(get_jwt_identity())
    data = request.get_json()
    order = create_order(user_id, data["total_amount"])

    return jsonify(id=order.id, status=order.status), 201


# -------------------------------------------------
# GET ORDER BY ID (USER)
# -------------------------------------------------
@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get(order_id):
    """
    Get Order by ID
    ---
    tags:
      - Orders
    description: |
      Fetch a single order using its ID.

      🔹 Beginner Notes:
      - Order ID is passed as URL path variable
      - JWT is required to access this API

    parameters:
      - in: path
        name: order_id
        required: true
        type: integer
        description: Order ID

    responses:
      200:
        description: Order details returned
      404:
        description: Order not found
    """
    order = get_order(order_id)

    return jsonify(
        id=order.id,
        amount=float(order.total_amount)
    )


# -------------------------------------------------
# LIST ALL ORDERS (USER)
# -------------------------------------------------
@order_bp.route("", methods=["GET"])
@jwt_required()
def list_all():
    """
    List Orders
    ---
    tags:
      - Orders
    description: |
      Returns all orders for the logged-in user.

      🔹 Beginner Notes:
      - JWT token identifies which user is calling
      - Pagination can be added later

    responses:
      200:
        description: List of orders
    """
    orders = list_orders()

    return jsonify([
        {
            "id": o.id,
            "amount": float(o.total_amount)
        }
        for o in orders
    ])


# -------------------------------------------------
# DELETE ORDER (USER)
# -------------------------------------------------
@order_bp.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete(order_id):
    """
    Delete Order
    ---
    tags:
      - Orders
    description: |
      Deletes an order using its ID.

      🔹 Beginner Notes:
      - This performs a hard delete
      - Soft delete can be added later

    parameters:
      - in: path
        name: order_id
        required: true
        type: integer
        description: Order ID

    responses:
      200:
        description: Order deleted successfully
      404:
        description: Order not found
    """
    delete_order(order_id)
    return jsonify(message="Order deleted")


# -------------------------------------------------
# LIST ALL ORDERS (ADMIN ONLY) WITH PAGINATION
# -------------------------------------------------
@order_bp.route("/admin/all", methods=["GET"])
@jwt_required()
@role_required(ROLE_ADMIN)
def admin_orders():
    """
    Get All Orders (Admin Only) - Paginated
    ---
    tags:
      - Orders
    description: |
      Returns all orders in the system with pagination support.

      🔹 Access:
      - Only ADMIN role can access this API

      🔹 Pagination:
      - page: Page number (default = 1)
      - size: Number of records per page (default = 10)

      Example:
      /orders/admin/all?page=1&size=10

      🔹 Beginner Notes:
      - Role validation is done by decorator
      - Pagination parameters come from query string

    parameters:
      - in: query
        name: page
        schema:
          type: integer
          example: 1
      - in: query
        name: size
        schema:
          type: integer
          example: 10

    responses:
      200:
        description: Paginated admin order list
      403:
        description: Access denied (not ADMIN)
    """

    # identity is always string in JWT
    user_id = int(get_jwt_identity())

    # Read pagination params
    page = request.args.get("page", default=1, type=int)
    size = request.args.get("size", default=10, type=int)

    # Call service layer
    orders, total = list_orders_paginated(page, size)

    return jsonify({
        "page": page,
        "size": size,
        "total_records": total,
        "data": [
            {
                "id": o.id,
                "status": o.status,
                "amount": float(o.total_amount)
            }
            for o in orders
        ]
    })


