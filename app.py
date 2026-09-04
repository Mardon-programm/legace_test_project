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
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S")


def chunked(items, size=100):
    for i in range(0, len(items), size):
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
    print("Fetched %s bytes from %s%s at %s" % (len(raw), host, path, format_timestamp()))

    api_url = "https://legacy.example.com/submit"
    total = save_legacy_users(chunked([{"id": i, "name": "user%d" % i} for i in range(5)]))
    print("Saved %d users" % total)


if __name__ == "__main__":
    main()
