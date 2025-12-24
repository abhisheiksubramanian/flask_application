from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.order_service import create_order, get_order, list_orders, delete_order
from app.security.decorators import role_required
from app.security.roles import ROLE_ADMIN

order_bp = Blueprint("orders", __name__)

@order_bp.route("", methods=["POST"])
@jwt_required()
def create():
    identity = get_jwt_identity()
    data = request.json
    order = create_order(identity["user_id"], data["total_amount"])
    return jsonify(id=order.id, status=order.status), 201

@order_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get(order_id):
    order = get_order(order_id)
    return jsonify(id=order.id, amount=order.total_amount)

@order_bp.route("", methods=["GET"])
@jwt_required()
def list_all():
    orders = list_orders()
    return jsonify([{"id": o.id, "amount": o.total_amount} for o in orders])

@order_bp.route("/<int:order_id>", methods=["DELETE"])
@jwt_required()
def delete(order_id):
    delete_order(order_id)
    return jsonify(message="Order deleted")

@order_bp.route("/admin/all", methods=["GET"])
@jwt_required()
@role_required(ROLE_ADMIN)
def admin_orders():
    """
    Get All Orders (Admin)
    ---
    tags:
      - Orders
    security:
      - Bearer: []
    responses:
      200:
        description: Admin order list
    """
    orders = list_orders()
    return jsonify([
        {"id": o.id, "status": o.status, "amount": float(o.total_amount)}
        for o in orders
    ])
