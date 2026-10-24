"""To-do list."""


class TodoList:
    def __init__(self):
        self._items = {}
        self._next = 1

    def add(self, title, priority):
        if priority not in (1, 2, 3):
            raise ValueError("priority is 1, 2 or 3")
        if not title.strip():
            raise ValueError("empty title")
        i = self._next
        self._next += 1
        self._items[i] = [title, priority, False]
        return i

    def done(self, id):
        if id not in self._items:
            raise KeyError(id)
        self._items[id][2] = True

    def open_items(self):
        return [t for t, p, d in self._items.values() if not d]

    def done_items(self):
        return [t for t, p, d in self._items.values() if d]

    def by_priority(self):
        rows = [(-p, i, t) for i, (t, p, d) in self._items.items() if not d]
        return [t for _, _, t in sorted(rows)]

    def rename(self, id, title):
        self._items[id][0] = title

    def remove(self, id):
        del self._items[id]
