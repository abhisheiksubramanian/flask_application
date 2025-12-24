from app.models.order import Order
from app.extensions.db import db

def save(order):
    db.session.add(order)
    db.session.commit()
    return order

def find_by_id(order_id):
    return Order.query.get(order_id)

def find_all():
    return Order.query.all()

def delete(order):
    db.session.delete(order)
    db.session.commit()
