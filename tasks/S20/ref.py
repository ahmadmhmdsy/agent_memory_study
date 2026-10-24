class Store:
    def __init__(self):
        self.stock = {}

    def add(self, name, qty):
        self.stock[name] = self.stock.get(name, 0) + qty

    def qty(self, name):
        return self.stock.get(name, 0)

    def names(self):
        return sorted(self.stock)

    def low_stock(self, threshold=5):
        return sorted(n for n, q in self.stock.items() if q < threshold)

    def total(self):
        return sum(self.stock.values())
