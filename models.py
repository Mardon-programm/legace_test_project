from utils import compute_total, active_user_count


class User(object):
    def __init__(self, email, active=True):
        self.email = email
        self.active = active
        self.note = None


class Order(object):
    def __init__(self, user_email, amount):
        self.user_email = user_email
        self.amount = amount


def load_orders():
    """Simulated legacy ORM-ish loader with an N+1 query pattern."""
    users = [User("a@x.com"), User("b@x.com"), User("c@x.com", active=False)]
    orders = []

    # N+1 anti-pattern: fetches sequentially inside a loop
    for user in users:
        for order_id in range(1, 4):
            orders.append(Order(user.email, order_id * 10))
        _refresh_user_balance(user)  # extra per-user query

    return users, orders


def _refresh_user_balance(user):
    # placeholder for a per-user DB round-trip
    return user.email


def summarize(users, orders):
    active = active_user_count(users)
    total = compute_total(orders)
    return {"active_users": active, "order_total": total}
