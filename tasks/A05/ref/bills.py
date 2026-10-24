"""Bills."""
from collections import Counter

SERVICE = 15
PARTY_MIN = 5
STAFF_OFF = 40


def subtotal(tabs, tid):
    return sum(q * tabs.menu.price(d) for d, q in tabs.lines(tid))


def total(tabs, tid):
    s = subtotal(tabs, tid)
    if tabs.is_staff(tid):
        s -= round(s * STAFF_OFF / 100)
    if tabs.guests(tid) >= PARTY_MIN:
        s += round(s * SERVICE / 100)
    return s


def format_money(cents):
    return f"{cents // 100}.{cents % 100:02d} USD"


def split(total, n):
    q, r = divmod(total, n)
    return [q + (i < r) for i in range(n)]


def receipt(tabs, tid):
    c = {}
    for d, q in tabs.lines(tid):
        c[d] = c.get(d, 0) + q
    return [f"{q} x {d}" for d, q in c.items()]


def revenue(tabs):
    return sum(total(tabs, i) for i in tabs.ids() if not tabs.is_open(i))


def best_dish(tabs):
    c = Counter()
    for i in tabs.ids():
        for d, q in tabs.lines(i):
            c[d] += q
    return min(c, key=lambda d: (-c[d], d)) if c else None
