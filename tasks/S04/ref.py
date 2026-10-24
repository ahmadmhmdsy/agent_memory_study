class InventoryError(Exception):
    pass


class Inventory:
    def __init__(self):
        self.stock = {}

    def add_stock(self, name, qty):
        self.stock[name] = self.stock.get(name, 0) + qty

    def quantity(self, name):
        return self.stock.get(name, 0)

    def total_items(self):
        return sum(self.stock.values())

    def remove_stock(self, name, qty):
        if qty > self.quantity(name):
            raise InventoryError(name)
        self.stock[name] -= qty
