from datetime import date


class TodoList:
    def __init__(self):
        self.items = []

    def add(self, title, priority, due=None):
        title = title.strip()
        if len(title) > 60:
            raise ValueError("title too long")
        if any(x["title"].lower() == title.lower() for x in self.items):
            raise ValueError("duplicate title")
        if type(priority) is not int or not 1 <= priority <= 3:
            raise ValueError("bad priority")
        if due is not None:
            if len(due) != 10:
                raise ValueError("bad due date")
            date.fromisoformat(due)
        tid = len(self.items) + 1
        self.items.append({"id": tid, "title": title, "priority": priority, "due": due, "done": False})
        return tid

    def tasks(self):
        return sorted(self.items, key=lambda x: (x["priority"], x["id"]))
