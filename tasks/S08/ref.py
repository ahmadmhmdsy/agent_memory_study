def is_freezing(c):
    return c <= 0


def count_above(readings, limit):
    return sum(1 for r in readings if r > limit)


def average(readings):
    return round(sum(readings) / len(readings) + 273.15, 2)
