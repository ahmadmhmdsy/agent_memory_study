from decimal import Decimal, ROUND_HALF_UP


def _hw(book, name):
    hw = book.scores(name, "hw")
    if len(hw) >= 3:
        hw = sorted(hw)[1:]
    return sum(hw) / len(hw)


def top_homework(book, n):
    names = [s for s in book.students() if book.scores(s, "hw")]
    return sorted(names, key=lambda s: -_hw(book, s))[:n]


def final_score(book, name):
    x = 0.5 * _hw(book, name) + 0.5 * book.scores(name, "exam")[-1]
    return int(Decimal(str(x)).quantize(Decimal(1), ROUND_HALF_UP))


def passed(book, name):
    return final_score(book, name) >= 60
