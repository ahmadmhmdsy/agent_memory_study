"""Late fees."""


def late_fee(lib, isbn, day):
    return min(500, max(0, day - lib.due(isbn)) * 25)
