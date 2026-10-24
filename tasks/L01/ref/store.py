class Store:
    def __init__(self):
        self.stock = {}

    def add(self, sku, qty):
        self.stock[sku] = self.stock.get(sku, 0) + qty

    def qty(self, sku):
        return self.stock.get(sku, 0)

    def skus(self):
        return sorted(self.stock)

    def total_units(self):
        return sum(self.stock.values())

    def remove(self, sku, qty):
        if type(qty) is not int or qty <= 0:
            raise ValueError("quantity must be a positive int")
        if qty > self.qty(sku):
            raise ValueError("not enough stock")
        self.stock[sku] -= qty
        if self.stock[sku] == 0:
            del self.stock[sku]
