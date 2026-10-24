"""Members and their points."""

SIGNUP = 75


class Members:
    def __init__(self):
        self._m = {}

    def add(self, name):
        if name in self._m:
            raise ValueError(f"{name} is already a member")
        self._m[name] = SIGNUP

    def points(self, name):
        return self._m[name]

    def add_points(self, name, n):
        self._m[name] += n

    def names(self):
        return sorted(self._m, key=str.lower)

    def remove(self, name):
        del self._m[name]

    def count(self):
        return len(self._m)

    def richest(self):
        return min(self._m, key=lambda n: (-self._m[n], n)) if self._m else None
