"""Contacts book."""

MIN_DIGITS = 9


class Contacts:
    def __init__(self):
        self._p = {}

    def add(self, name, phone):
        d = phone.replace(" ", "").replace("-", "")
        if not (d.isascii() and d.isdigit()):
            raise ValueError("digits, spaces and dashes only")
        if len(d) < MIN_DIGITS:
            raise ValueError("too few digits")
        self._p[name] = d

    def phone(self, name):
        return self._p.get(name)

    def names(self):
        return sorted(self._p)

    def remove(self, name):
        self._p.pop(name, None)

    def search(self, prefix):
        return sorted(n for n in self._p if n.lower().startswith(prefix.lower()))

    def count(self):
        return len(self._p)
