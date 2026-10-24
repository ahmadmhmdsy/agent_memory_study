def clamp_score(s):
    return max(0, min(100, s))


def best(scores):
    return max(scores)


def average(scores):
    return int(sum(scores) / len(scores))
