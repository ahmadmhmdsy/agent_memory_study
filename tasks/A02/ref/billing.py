"""Prices and bills."""
import datetime as dt
from collections import Counter

RATE = 9900
TOURIST_TAX = 200


def night_price(day):
    return round(RATE * 1.2) if day.weekday() == 5 else RATE


def nights(booking):
    _, _, a, b = booking
    return [a + dt.timedelta(i) for i in range((b - a).days)]


def price(bookings, bid):
    return sum(night_price(d) for d in nights(bookings.get(bid)))


def bill(bookings, bid):
    return price(bookings, bid) + TOURIST_TAX * len(nights(bookings.get(bid)))


def invoice(bookings, bid):
    lines = [f"{d.isoformat()}: {night_price(d)}" for d in nights(bookings.get(bid))]
    return lines + [f"total: {bill(bookings, bid)}"]


def revenue(bookings):
    return sum(bill(bookings, i) for i in bookings.ids())


def busiest_day(bookings):
    c = Counter(d for i in bookings.ids() for d in nights(bookings.get(i)))
    return min(c, key=lambda d: (-c[d], d)) if c else None
