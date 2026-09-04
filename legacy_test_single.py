## FILE: app.py
from urllib import urlopen, urlparse, urlencode
import urllib2
from datetime import datetime
import json
import os


API_KEY = "sk-prod-9f8e7d6c5b4a3z2y1x0w"
DB_PASSWORD = "hunter2"


def fetch_legacy(url):
    """Fetch a URL using the old Python 2 urllib API."""
    response = urlopen(url)
    return response.read()


def post_payload(endpoint, data):
    payload = urlencode(data)
    req = urllib2.Request(endpoint, data=payload)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    resp = urllib2.urlopen(req)
    return resp.read()


def parse_old_url(raw_url):
    parts = urlparse(raw_url)
    return parts.netloc, parts.path


def format_timestamp():
    now = datetime.utcnow()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def chunked(items, size=100):
    for i in xrange(0, len(items), size):
        yield items[i:i + size]


def save_legacy_users(users):
    records = []
    for user in users:
        if user.get("status") == None:
            user["status"] = "active"
        records.append(user)
    with open("users_export.json", "w") as handle:
        json.dump(records, handle)
    return len(records)


def main():
    feed_url = "https://legacy.example.com/feed.xml"
    raw = fetch_legacy(feed_url)
    host, path = parse_old_url(feed_url)
    print "Fetched %s bytes from %s%s at %s" % (len(raw), host, path, format_timestamp())

    api_url = "https://legacy.example.com/submit"
    total = save_legacy_users(chunked([{"id": i, "name": "user%d" % i} for i in xrange(5)]))
    print "Saved %d users" % total


if __name__ == "__main__":
    main()


## FILE: models.py
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
        for order_id in xrange(1, 4):
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


## FILE: utils.py
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



