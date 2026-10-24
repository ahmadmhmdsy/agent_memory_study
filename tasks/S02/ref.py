def mean(scores):
    return sum(scores) / len(scores)


def median(scores):
    s = sorted(scores)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def unique_scores(scores):
    return sorted(set(scores), reverse=True)
