"""In-memory todo list."""


class TodoList:
    def __init__(self):
        self.items = []
        self._next_id = 1

    def add(self, title):
        item = {"id": self._next_id, "title": title, "done": False}
        self.items.append(item)
        self._next_id += 1
        return item["id"]

    def done(self, todo_id):
        for item in self.items:
            if item["id"] == todo_id:
                item["done"] = True
                return
        raise KeyError(todo_id)

    def pending(self):
        return [i for i in self.items if not i["done"]]
