from flask import Flask
from app.config.dev import DevConfig
from app.extensions.db import db
from app.extensions.jwt import jwt
from app.extensions.bcrypt import bcrypt
from app.controllers.auth_controller import auth_bp
from app.controllers.order_controller import order_bp
from app.exceptions.handlers import register_error_handlers
from app.extensions.swagger import swagger


def create_app(testing=False):
    app = Flask(__name__)

    if testing:
        app.config["TESTING"] = True  

    app.config.from_object(DevConfig)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(order_bp, url_prefix="/orders")

    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app
 
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


def create_app(testing=False):
    app = Flask(__name__)

    # ---------------------------------
    # Configuration
    # ---------------------------------
    if testing:
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            JWT_SECRET_KEY="test-secret",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
        )
    else:
        app.config.from_object(DevConfig)

    # ---------------------------------
    # Initialize Extensions
    # ---------------------------------
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    swagger.init_app(app)

    # ---------------------------------
    # Register Blueprints
    # ---------------------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(order_bp, url_prefix="/orders")

    # ---------------------------------
    # Register Error Handlers
    # ---------------------------------
    register_error_handlers(app)

    return app


# ---------------------------------
# Application Entry Point
# ---------------------------------
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # OK for local/dev only

    app.run(host="0.0.0.0", port=5000, debug=True)
