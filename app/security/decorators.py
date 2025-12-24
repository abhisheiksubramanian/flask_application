from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.security.roles import ROLE_ADMIN

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if not identity or identity.get("role") != required_role:
                return jsonify(error="Access denied"), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
