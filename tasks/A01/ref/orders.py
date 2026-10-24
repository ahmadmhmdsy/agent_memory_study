"""Customer orders."""
from stock import normalize_sku


class Orders:
    def __init__(self, stock):
        self.stock = stock
        self._o = {}
        self._n = 0

    def place(self, sku, qty, day):
        if qty < 1:
            raise ValueError("quantity must be 1 or more")
        sku = normalize_sku(sku)
        self.stock.remove(sku, qty)
        self._n += 1
        oid = f"O-{self._n:04d}"
        self._o[oid] = (sku, qty, day)
        return oid

    def get(self, oid):
        return self._o[oid]

    def cancel(self, oid):
        sku, qty, _ = self._o.pop(oid)
        self.stock.add(sku, qty)

    def ids(self):
        return list(self._o)

    def of_day(self, day):
        return [k for k, v in self._o.items() if v[2] == day]

    def open_count(self):
        return len(self._o)

    def history(self, sku):
        sku = normalize_sku(sku)
        return [k for k, v in self._o.items() if v[0] == sku]

    def total_items(self):
        return sum(v[1] for v in self._o.values())
