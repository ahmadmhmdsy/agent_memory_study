import json
from todo import TodoList


def save(todo, path):
    with open(path, "w") as f:
        json.dump({"version": 2, "tasks": todo.items}, f, indent=2)


def load(path):
    with open(path) as f:
        d = json.load(f)
    t = TodoList()
    t.items = d["tasks"]
    return t
