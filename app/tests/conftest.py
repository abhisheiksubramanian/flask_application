import pytest
from app.main import create_app
from app.extensions.db import db

@pytest.fixture
def app():
    app = create_app(testing=True)

    app.config.update(
        TESTING=True,
        JWT_SECRET_KEY="test-secret",
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
