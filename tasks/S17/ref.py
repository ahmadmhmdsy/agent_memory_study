class Stack:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop()

    def __len__(self):
        return len(self.items)

    def is_empty(self):
        return not self.items

    def clear(self):
        self.items.clear()

    def peek(self):
        return self.items[-1] if self.items else None

    def to_list(self):
        return list(self.items)
