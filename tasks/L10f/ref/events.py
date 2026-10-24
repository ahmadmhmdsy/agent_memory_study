import re
from datetime import date


def parse_date(s):
    s = s.strip()
    if "." in s:
        d, m, y = s.split(".")
    else:
        y, m, d = s.split("-")
    return date(int(y), int(m), int(d))


class Event:
    def __init__(self, name, date, capacity, price):
        self.name = name
        self.date = date
        self.capacity = capacity
        self.price = price
        self.sold = 0

    def seats_left(self):
        return self.capacity - self.sold


def upcoming(events, today):
    return [e.name for e in sorted((e for e in events if e.date >= today), key=lambda e: (e.date, e.name))]


def slug(name):
    return "-".join(re.findall(r"[a-z0-9]+", name.lower()))
