from flask_jwt_extended import create_access_token
from app.repositories.user_repo import find_by_username, save
from app.models.user import User
from app.extensions.bcrypt import bcrypt
from app.exceptions.business import BusinessException

def register_user(username, password):
    if find_by_username(username):
        raise BusinessException("User already exists")

    hashed = bcrypt.generate_password_hash(password).decode()
    user = User(username=username, password=hashed)
    save(user)

def login_user(username, password):
    user = find_by_username(username)

    if not user or not bcrypt.check_password_hash(user.password, password):
        raise BusinessException("Invalid credentials")

    return create_access_token(
        identity={"user_id": user.id, "role": user.role}
    )
