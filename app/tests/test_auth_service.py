import pytest
from app.services.auth_service import register_user, login_user
from app.exceptions.business import BusinessException

def test_register_service(app):
    with app.app_context():
        register_user("svcuser", "pass123")

def test_register_duplicate_user(app):
    with app.app_context():
        register_user("svcuser", "pass123")
        with pytest.raises(BusinessException):
            register_user("svcuser", "pass123")

def test_login_service(app):
    with app.app_context():
        register_user("svcuser", "pass123")
        token = login_user("svcuser", "pass123")
        assert token is not None
