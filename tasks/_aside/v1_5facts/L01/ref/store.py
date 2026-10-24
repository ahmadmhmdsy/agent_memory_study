class Store:
    def __init__(self):
        self.stock = {}

    def add(self, sku, qty):
        self.stock[sku] = self.stock.get(sku, 0) + qty

    def qty(self, sku):
        return self.stock.get(sku, 0)

    def skus(self):
        return sorted(self.stock)

    def remove(self, sku, qty):
        if qty > self.qty(sku):
            raise ValueError("not enough stock")
        self.stock[sku] -= qty
        if self.stock[sku] == 0:
            del self.stock[sku]
