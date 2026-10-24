class Gradebook:
    def __init__(self):
        self.scores = {}

    def add_score(self, student_id, score):
        if not 0 <= score <= 100:
            raise ValueError("score out of range")
        self.scores.setdefault(student_id.upper(), []).append(score)

    def average(self, student_id):
        s = self.scores.get(student_id.upper())
        return round(sum(s) / len(s), 1) if s else None

    def ranking(self):
        return sorted(self.scores, key=lambda i: (-self.average(i), i))
