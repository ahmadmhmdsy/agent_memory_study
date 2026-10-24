from questions import parse_answer
from grading import grade


class Quiz:
    def __init__(self, title):
        self.title = title
        self.qs = []
        self.ans = {}

    def add_question(self, text, correct):
        self.qs.append(parse_answer(correct))
        return len(self.qs)

    def answer(self, name, number, letter):
        l = parse_answer(letter)
        a = self.ans.setdefault(name, {})
        if number in a:
            raise ValueError("already answered")
        a[number] = l

    def score(self, name):
        a = self.ans[name]
        r = sum(1 for i, c in enumerate(self.qs, 1) if a.get(i) == c)
        return 4 * r - 2 * (len(self.qs) - r)

    def percent(self, name):
        return max(0, self.score(name)) * 100 / (4 * len(self.qs))

    def ranking(self):
        return sorted(self.ans, key=lambda n: (-self.score(n), n))

    def players(self):
        return sorted(self.ans)

    def passed(self, name):
        return grade(self.percent(name)) != "F"
