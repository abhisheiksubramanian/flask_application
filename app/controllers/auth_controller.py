"""
=========================================================
AUTH CONTROLLER – AUTH SERVICE
=========================================================

This file contains all authentication-related APIs.

📌 What this controller provides:
--------------------------------
1. User Registration
2. User Login (JWT Token)
3. Health Check API

📌 Technologies used:
--------------------
- Flask Blueprint (modular API design)
- JWT Authentication (handled in service layer)
- Swagger UI (via Flasgger)
- Custom BusinessException handling

📌 How Swagger works here:
--------------------------
- Swagger UI reads the YAML written inside docstrings
- `parameters: in: body` is used to show input boxes
- OpenAPI 3 `requestBody` is NOT used because Flasgger UI
  does not reliably render input fields for it

📌 Swagger URL:
---------------
http://127.0.0.1:5000/apidocs/

=========================================================
"""

from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.exceptions.business import BusinessException

# -------------------------------------------------
# Blueprint definition
# -------------------------------------------------
auth_bp = Blueprint("auth", __name__)


# -------------------------------------------------
# REGISTER USER API
# -------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register User
    ---
    tags:
      - Auth
    description: |
      This API registers a new user into the system.

      🔹 Flow:
      1. Client sends username & password
      2. Password is hashed in service layer
      3. User is stored in database

      🔹 Notes for beginners:
      - Password hashing is NOT done here
      - Business logic is kept inside `auth_service`

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
      400:
        description: User already exists or invalid input
    """
    try:
        data = request.get_json()
        register_user(data["username"], data["password"])
        return jsonify(message="User registered"), 201
    except BusinessException as e:
        return jsonify(error=str(e)), 400


# -------------------------------------------------
# LOGIN USER API
# -------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login User
    ---
    tags:
      - Auth
    description: |
      This API authenticates a user and returns a JWT token.

      🔹 Flow:
      1. Client sends username & password
      2. Credentials are validated in service layer
      3. JWT token is generated and returned

      🔹 What is JWT?
      - JSON Web Token
      - Used to access protected APIs

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
        description: JWT token generated successfully
      401:
        description: Invalid credentials
    """
    try:
        data = request.get_json()
        token = login_user(data["username"], data["password"])
        return jsonify(access_token=token)
    except BusinessException as e:
        return jsonify(error=str(e)), 401


# -------------------------------------------------
# HEALTH CHECK API
# -------------------------------------------------
@auth_bp.route("/health", methods=["GET"])
def health():
    """
    Health Check
    ---
    tags:
      - Health
    description: |
      This API is used to check whether the service is running.

      🔹 Commonly used by:
      - Load balancers
      - Monitoring tools
      - DevOps health probes

    responses:
      200:
        description: Service is running
    """
    return jsonify(status="UP")
