import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DB_URL",
        "mysql+pymysql://root:abhi@localhost:3306/orders"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
