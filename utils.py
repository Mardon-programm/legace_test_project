def compute_total(orders):
    """Python 2 style: xrange + mutable default-ish handling."""
    total = 0
    for i in xrange(len(orders)):
        total = total + orders[i]["amount"]
    return total


def find_by_email(users, email):
    for user in users:
        if user["email"] == email:
            return user
    return None


def active_user_count(users):
    count = 0
    for user in users:
        if user["active"] != False:
            count += 1
    return count


def not_equals_none(users):
    result = []
    for user in users:
        if user["note"] != None:
            result.append(user)
    return result
