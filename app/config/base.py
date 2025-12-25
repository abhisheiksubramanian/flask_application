import os

class BaseConfig:
    DEBUG = True

    # 🔐 JWT Secret Key (REQUIRED)
    JWT_SECRET_KEY = "super-secret-jwt-key"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:abhi@localhost/orders"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    TESTING = True
