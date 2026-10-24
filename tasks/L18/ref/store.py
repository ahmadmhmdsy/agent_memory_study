import random
import re
import string
from urls import domain_of, normalize

ALPHA = "".join(c for c in string.ascii_letters + string.digits if c not in "0O1lI")


class Shortener:
    def __init__(self):
        self.links = {}
        self.clicks = {}

    def _new_code(self):
        while True:
            c = "".join(random.choice(ALPHA) for _ in range(7))
            if c not in self.links:
                return c

    def shorten(self, url, today, alias=None):
        u = normalize(url)
        if alias is None:
            for c, (lu, cr) in self.links.items():
                if lu == u:
                    return c
            c = self._new_code()
        else:
            if not re.fullmatch(r"[A-Za-z0-9-]{3,20}", alias) or alias in self.links:
                raise ValueError("bad alias")
            c = alias
        self.links[c] = (u, today)
        self.clicks[c] = []
        return c

    def _live(self, code, today):
        return code in self.links and (today - self.links[code][1]).days < 90

    def expand(self, code, today):
        if not self._live(code, today):
            return None
        self.clicks[code].append(today)
        return self.links[code][0]

    def delete(self, code):
        self.links.pop(code, None)

    def stats(self, code, day=None):
        cl = self.clicks[code]
        return len(cl) if day is None else cl.count(day)

    def count(self, today):
        return sum(1 for c in self.links if self._live(c, today))

    def by_domain(self):
        out = {}
        for u, cr in self.links.values():
            d = domain_of(u)
            out[d] = out.get(d, 0) + 1
        return out
