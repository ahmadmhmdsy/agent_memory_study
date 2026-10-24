KINDS = ("run", "bike", "swim")


def check_minutes(m):
    if not isinstance(m, int) or not 1 <= m <= 300:
        raise ValueError("bad duration")


def check_kind(kind):
    k = kind.strip().lower()
    if k not in KINDS:
        raise ValueError("unknown kind")
    return k


class Log:
    def __init__(self):
        self.data = {}

    def add(self, day, kind, minutes, km=0):
        k = check_kind(kind)
        check_minutes(minutes)
        e = self.data.setdefault(day, {}).setdefault(k, [0, 0])
        e[0] += minutes
        e[1] += km

    def entries(self, day):
        return [(k, m, km) for k, (m, km) in self.data.get(day, {}).items()]

    def total(self, kind=None):
        return sum(m for d in self.data.values() for k, (m, km) in d.items() if kind is None or k == kind)

    def days(self):
        return sorted(self.data)

    def kinds(self):
        t = {}
        for d in self.data.values():
            for k, (m, km) in d.items():
                t[k] = t.get(k, 0) + m
        return sorted(t, key=lambda k: -t[k])
