"""Order fees."""

BASE = 329
PER_KM = 45
FREE_OVER = 2500
SERVICE = 6
RUSH = 150


def subtotal(orders, oid):
    rest, items, _, _ = orders.get(oid)
    return sum(orders.restaurants.price(rest, d) * q for d, q in items)


def delivery_fee(orders, oid):
    if subtotal(orders, oid) >= FREE_OVER:
        return 0
    return BASE + PER_KM * orders.get(oid)[2]


def service_fee(orders, oid):
    return round(subtotal(orders, oid) * SERVICE / 100)


def total(orders, oid):
    rush = RUSH if 1080 <= orders.get(oid)[3] <= 1199 else 0
    return subtotal(orders, oid) + delivery_fee(orders, oid) + service_fee(orders, oid) + rush


def revenue(orders):
    return sum(total(orders, k) for k in orders.at_status("delivered"))
