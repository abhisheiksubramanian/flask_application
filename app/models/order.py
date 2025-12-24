from app.extensions.db import db

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(30), default="CREATED")
    total_amount = db.Column(db.Float, nullable=False)
