from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.exceptions.business import BusinessException

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register User
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: abhi
              password:
                type: string
                example: secret123
    responses:
      201:
        description: User registered successfully
      400:
        description: User already exists or invalid input
    """
    try:
        data = request.get_json()
        register_user(data["username"], data["password"])
        return jsonify(message="User registered"), 201
    except BusinessException as e:
        return jsonify(error=str(e)), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login User
    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: abhi
              password:
                type: string
                example: secret123
    responses:
      200:
        description: JWT token generated
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        token = login_user(data["username"], data["password"])
        return jsonify(access_token=token)
    except BusinessException as e:
        return jsonify(error=str(e)), 401


@auth_bp.route("/health", methods=["GET"])
def health():
    """
    Health Check
    ---
    tags:
      - Health
    responses:
      200:
        description: Service is running
    """
    return jsonify(status="UP")
