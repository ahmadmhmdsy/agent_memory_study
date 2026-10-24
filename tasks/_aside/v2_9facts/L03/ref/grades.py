class Gradebook:
    def __init__(self):
        self.scores = {}

    def add_score(self, student_id, score):
        if type(score) is not int:
            raise TypeError("score must be an int")
        if not 0 <= score <= 100:
            raise ValueError("score out of range")
        s = self.scores.setdefault(student_id.upper(), [])
        if len(s) >= 10:
            raise ValueError("too many scores")
        s.append(score)

    def average(self, student_id):
        s = self.scores.get(student_id.upper())
        return round(sum(s) / len(s), 1) if s else None

    def ranking(self):
        ids = [i for i, s in self.scores.items() if len(s) >= 2]
        return sorted(ids, key=lambda i: (-self.average(i), i))
