"""Stock levels."""
import re

REORDER_BELOW = 8
MAX_ITEMS = 1000


def normalize_sku(s):
    s = s.replace("-", "").replace(" ", "").upper()
    if not re.fullmatch(r"[A-Z0-9]{1,12}", s):
        raise ValueError(f"bad SKU {s!r}")
    return s


class Stock:
    def __init__(self):
        self._c = {}

    def add(self, sku, n):
        sku = normalize_sku(sku)
        if self._c.get(sku, 0) + n > MAX_ITEMS:
            raise ValueError("too many items")
        self._c[sku] = self._c.get(sku, 0) + n

    def count(self, sku):
        return self._c.get(normalize_sku(sku), 0)

    def remove(self, sku, n):
        sku = normalize_sku(sku)
        if n > self._c.get(sku, 0):
            raise ValueError("not enough stock")
        self._c[sku] -= n

    def skus(self):
        return sorted(k for k, v in self._c.items() if v > 0)

    def value(self, prices):
        return sum(v * prices[k] for k, v in self._c.items() if v > 0)

    def rename(self, old, new):
        old, new = normalize_sku(old), normalize_sku(new)
        if self._c.get(new, 0) > 0:
            raise ValueError("target in stock")
        self._c[new] = self._c.pop(old, 0)


def needs_reorder(stock):
    return [k for k in stock.skus() if stock.count(k) < REORDER_BELOW]
