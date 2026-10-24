def parse_score(s):
    s = s.strip()
    if s.endswith("%"):
        return float(s[:-1])
    a, b = s.split("/")
    return float(a) / float(b) * 100


def _clean(name):
    return " ".join(name.split())


class Gradebook:
    def __init__(self):
        self.data = {}

    def add_student(self, name):
        name = _clean(name)
        if name in self.data:
            raise ValueError("student already exists")
        self.data[name] = {"hw": [], "exam": []}

    def add_score(self, name, kind, score):
        if not 0 <= score <= 100:
            raise ValueError("score out of range")
        self.data[_clean(name)][kind].append(score)

    def scores(self, name, kind):
        return list(self.data[_clean(name)][kind])

    def students(self):
        return sorted(self.data)

    def count(self, name):
        d = self.data[_clean(name)]
        return len(d["hw"]) + len(d["exam"])
