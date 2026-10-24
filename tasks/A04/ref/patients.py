"""Patients."""


class Patients:
    def __init__(self):
        self._p = {}
        self._n = 0

    @staticmethod
    def _clean(name):
        name = " ".join(w for w in name.split(" ") if w)
        if not name:
            raise ValueError("name required")
        return name

    def register(self, name, age):
        name = self._clean(name)
        self._n += 1
        self._p[self._n] = [name, age]
        return self._n

    def name(self, pid):
        return self._p[pid][0]

    def age(self, pid):
        return self._p[pid][1]

    def find(self, text):
        return [k for k, v in self._p.items() if text.lower() in v[0].lower()]

    def rename(self, pid, name):
        self._p[pid][0] = self._clean(name)
