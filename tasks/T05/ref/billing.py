"""Class billing."""

PRICE = 950


def bill(schedule, member):
    return len(schedule.busy(member)) * PRICE
