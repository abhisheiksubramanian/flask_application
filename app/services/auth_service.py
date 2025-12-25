from flask_jwt_extended import create_access_token
from app.repositories.user_repo import find_by_username, save
from app.models.user import User
from app.extensions.bcrypt import bcrypt
from app.exceptions.business import BusinessException


def register_user(username, password):
    """
    Registers a new user.

    - Checks if username already exists
    - Hashes password
    - Saves user to database
    """
    if find_by_username(username):
        raise BusinessException("User already exists")

    hashed = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed)
    save(user)


def login_user(username, password):
    """
    Authenticates user and generates JWT token.

    JWT Design (Best Practice):
    ---------------------------
    - identity (sub)  : user_id as STRING
    - additionalClaims: role (ADMIN / USER)

    This avoids JWT spec violations and works
    correctly with Flask-JWT-Extended.
    """
    user = find_by_username(username)

    if not user or not bcrypt.check_password_hash(user.password, password):
        raise BusinessException("Invalid credentials")

    # ✅ Correct JWT creation
    access_token = create_access_token(
        identity=str(user.id),          # MUST be string
        additional_claims={
            "role": user.role           # extra info goes here
        }
    )

    return access_token
