"""Reports."""
from collections import Counter

from stock import needs_reorder


def top_skus(orders, n):
    c = Counter()
    for oid in orders.ids():
        sku, qty, _ = orders.get(oid)
        c[sku] += qty
    return [k for k, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))][:n]


def daily_items(orders):
    c = Counter()
    for oid in orders.ids():
        _, qty, day = orders.get(oid)
        c[day] += qty
    return dict(c)


def low_stock_summary(stock):
    return f"{len(needs_reorder(stock))} SKUs need reordering"
