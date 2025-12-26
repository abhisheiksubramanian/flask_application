"""
=========================================================
AUTH CONTROLLER – AUTH SERVICE
=========================================================

Provides authentication-related APIs:
1. Register User
2. Login User (JWT)
3. Health Check

Swagger UI:
http://127.0.0.1:5000/apidocs/

IMPORTANT:
- Flasgger requires `parameters: in: body`
- OpenAPI 3 `requestBody` is NOT used
=========================================================
"""

from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.exceptions.business import BusinessException

# -------------------------------------------------
# Blueprint
# -------------------------------------------------
auth_bp = Blueprint("auth", __name__)

# -------------------------------------------------
# REGISTER USER
# -------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register User
    ---
    tags:
      - Auth
    description: |
      Registers a new user in the system.

      🔹 Flow:
      1. Validate request body
      2. Hash password (service layer)
      3. Save user to database

      🔹 Validation:
      - username (required)
      - password (required)

    parameters:
      - in: body
        name: body
        required: true
        description: User registration payload
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
        schema:
          type: object
          properties:
            message:
              type: string
              example: User registered
      400:
        description: Invalid input or user already exists
        schema:
          type: object
          properties:
            error:
              type: string
              example: Username and password are required
    """
    try:
        data = request.get_json()

        # ✅ INPUT VALIDATION (Swagger + pytest safe)
        if not data or "username" not in data or "password" not in data:
            return jsonify(error="Username and password are required"), 400

        register_user(data["username"], data["password"])
        return jsonify(message="User registered"), 201

    except BusinessException as e:
        return jsonify(error=str(e)), 400


# -------------------------------------------------
# LOGIN USER
# -------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login User
    ---
    tags:
      - Auth
    description: |
      Authenticates a user and returns a JWT token.

      🔹 JWT:
      - Token must be sent in Authorization header
      - Format: Bearer <JWT>

    parameters:
      - in: body
        name: body
        required: true
        description: Login credentials
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
        schema:
          type: object
          properties:
            access_token:
              type: string
              example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
      400:
        description: Missing input fields
        schema:
          type: object
          properties:
            error:
              type: string
              example: Username and password are required
      401:
        description: Invalid credentials
        schema:
          type: object
          properties:
            error:
              type: string
              example: Invalid credentials
    """
    try:
        data = request.get_json()

        # ✅ INPUT VALIDATION
        if not data or "username" not in data or "password" not in data:
            return jsonify(error="Username and password are required"), 400

        token = login_user(data["username"], data["password"])
        return jsonify(access_token=token), 200

    except BusinessException as e:
        return jsonify(error=str(e)), 401


# -------------------------------------------------
# HEALTH CHECK
# -------------------------------------------------
@auth_bp.route("/health", methods=["GET"])
def health():
    """
    Health Check
    ---
    tags:
      - Health
    description: |
      Checks whether the service is running.

      Used by:
      - Load balancers
      - Monitoring systems
      - DevOps probes

    responses:
      200:
        description: Service is UP
        schema:
          type: object
          properties:
            status:
              type: string
              example: UP
    """
    return jsonify(status="UP"), 200
