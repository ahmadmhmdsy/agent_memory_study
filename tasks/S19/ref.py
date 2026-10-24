def clamp(score):
    return max(0, min(100, score))


def mean(scores):
    return sum(scores) / len(scores)


def highest(scores):
    return max(scores)


def letter(score):
    return "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "F"


def spread(scores):
    return max(scores) - min(scores)
