def total(lines):
    return sum(l["price"] * l["qty"] for l in lines)


def count_items(lines):
    return sum(l["qty"] for l in lines)


def discount_rate(order_total):
    return 0.1 if order_total >= 200 else 0.05 if order_total >= 100 else 0


def growth(old, new):
    return round((new - old) / old, 4)
