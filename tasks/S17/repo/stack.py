"""Stack for an undo feature."""


class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)
