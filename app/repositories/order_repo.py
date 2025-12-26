from app.models.order import Order
from app.extensions.db import db

def save(order):
    db.session.add(order)
    db.session.commit()
    return order

def find_by_id(order_id):
    # return Order.query.get(order_id)
    return db.session.get(Order, order_id)

def find_all():
    return Order.query.all()

def delete(order):
    db.session.delete(order)
    db.session.commit()


def get_orders_paginated(page, size):
    query = Order.query

    total = query.count()

    orders = query.offset((page - 1) * size).limit(size).all()

    return orders, total
