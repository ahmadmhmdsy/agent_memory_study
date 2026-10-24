"""Shopping cart."""


class Cart:
    def __init__(self):
        self._q = {}

    def add(self, sku, qty):
        if qty <= 0:
            raise ValueError("quantity must be positive")
        sku = sku.upper()
        self._q[sku] = self._q.get(sku, 0) + qty

    def count(self, sku):
        return self._q.get(sku.upper(), 0)

    def remove(self, sku, qty):
        sku = sku.upper()
        left = self._q.get(sku, 0) - qty
        if left > 0:
            self._q[sku] = left
        else:
            self._q.pop(sku, None)

    def items(self):
        return sorted(self._q.items())

    def clear(self):
        self._q.clear()

    def size(self):
        return sum(self._q.values())
