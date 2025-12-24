from flask import Flask
from app.config.dev import DevConfig
from app.extensions.db import db
from app.extensions.jwt import jwt
from app.extensions.bcrypt import bcrypt
from app.controllers.auth_controller import auth_bp
from app.controllers.order_controller import order_bp
from app.exceptions.handlers import register_error_handlers
from app.extensions.swagger import swagger


def create_app():
    app = Flask(__name__)
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
