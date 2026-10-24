"""The meters."""
import re


def _num(mid):
    return int(mid[1:])


class Meters:
    def __init__(self):
        self._m = {}

    def add(self, mid, social=False):
        if not re.fullmatch(r"M[0-9]+", mid):
            raise ValueError(f"bad meter id {mid!r}")
        self._m[mid] = social

    def is_social(self, mid):
        return self._m[mid]

    def set_social(self, mid, flag):
        self._m[mid]
        self._m[mid] = flag

    def ids(self):
        return sorted(self._m, key=_num)

    def remove(self, mid):
        del self._m[mid]

    def social_ids(self):
        return [m for m in self.ids() if self._m[m]]

    def count(self):
        return len(self._m)
