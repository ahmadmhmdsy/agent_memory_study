class Recipe:
    def __init__(self, name, servings):
        self.name = name
        self.servings = servings
        self._items = []

    def add(self, name, qty, unit):
        if qty <= 0:
            raise ValueError("quantity must be positive")
        name = name.strip().lower()
        for i, (n, q, u) in enumerate(self._items):
            if n == name:
                if u != unit:
                    raise ValueError("unit mismatch")
                self._items[i] = (n, q + qty, u)
                return
        self._items.append((name, qty, unit))

    def items(self):
        return list(self._items)

    def remove(self, name):
        name = name.strip().lower()
        for i, (n, _, _) in enumerate(self._items):
            if n == name:
                del self._items[i]
                return True
        return False

    def count(self):
        return len(self._items)
