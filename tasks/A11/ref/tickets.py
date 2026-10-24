"""Ticket prices."""

REGULAR = 22000
STUDENT_PCT = 40


def ticket_price(kind):
    if kind == "regular":
        return REGULAR
    if kind == "student":
        return round(REGULAR * STUDENT_PCT / 100)
    if kind == "speaker":
        return 0
    raise ValueError(f"unknown kind {kind!r}")
