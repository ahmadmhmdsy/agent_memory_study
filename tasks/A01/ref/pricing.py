"""Order prices."""

BULK = 7
TAX = 6
SHIPPING = 300


def price_line(qty, unit_cents):
    s = qty * unit_cents
    if qty >= 100:
        return round(s * (100 - BULK) / 100)
    return s


def order_total(qty, unit_cents):
    p = price_line(qty, unit_cents)
    return p + round(p * TAX / 100) + SHIPPING
