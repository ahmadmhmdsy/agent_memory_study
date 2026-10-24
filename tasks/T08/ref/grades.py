"""Grade book."""


class Gradebook:
    def __init__(self):
        self._s = {}

    def add(self, student, score):
        if not isinstance(score, int) or isinstance(score, bool) or not 0 <= score <= 100:
            raise ValueError("a score is an int from 0 to 100")
        if len(self._s.get(student, [])) >= 10:
            raise ValueError("at most 10 scores")
        self._s.setdefault(student, []).append(score)

    def scores(self, student):
        return list(self._s.get(student, []))

    def students(self):
        return sorted(self._s)

    def clear(self, student):
        self._s.pop(student, None)
