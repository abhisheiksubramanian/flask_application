from app.models.order import Order
from app.repositories import order_repo
from app.exceptions.business import BusinessException
from app.models.order import Order
from app.utils.pagination import paginate

def create_order(user_id, total_amount):
    if total_amount <= 0:
        raise BusinessException("Invalid amount")

    order = Order(user_id=user_id, total_amount=total_amount)
    return order_repo.save(order)

def get_order(order_id):
    order = order_repo.find_by_id(order_id)
    if not order:
        raise BusinessException("Order not found")
    return order

def list_orders():
    return order_repo.find_all()

def delete_order(order_id):
    order = get_order(order_id)
    order_repo.delete(order)


# def list_orders_paginated(status=None, page=1, size=10):
#     query = Order.query

#     if status:
#         query = query.filter_by(status=status)

#     pagination = paginate(query, page, size)

#     return {
#         "items": pagination.items,
#         "total": pagination.total,
#         "page": pagination.page,
#         "pages": pagination.pages
#     }

def list_orders_paginated(page, size):
    return order_repo.get_orders_paginated(page, size)