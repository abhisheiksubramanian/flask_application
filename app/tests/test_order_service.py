from app.services.order_service import create_order, list_orders_paginated

def test_create_order_service(app):
    with app.app_context():
        order = create_order(user_id=1, total_amount=1000)
        assert order.id is not None

def test_list_orders_paginated(app):
    with app.app_context():
        create_order(1, 100)
        create_order(1, 200)

        orders, total = list_orders_paginated(page=1, size=1)

        assert total == 2
        assert len(orders) == 1
