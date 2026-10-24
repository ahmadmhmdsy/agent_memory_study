"""To-do views."""


def summary(todo):
    n = len(todo.open_items())
    if n == 0:
        return "all done"
    return f"{n} open, {len(todo.done_items())} done"
