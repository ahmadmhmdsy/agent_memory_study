"""When plants are due."""
import datetime as dt

WATER = {"herb": 3, "cactus": 21, "fern": 5}
FEED = 28
ALARM_BELOW = 6


def next_water(care, name):
    last = care.last_watered(name)
    if last is None:
        return care.plants.added(name)
    return last + dt.timedelta(WATER[care.plants.kind(name)])


def next_feed(care, name):
    f = care.feedings(name)
    if not f:
        return care.plants.added(name)
    return f[-1] + dt.timedelta(FEED)


def due(care, day):
    names = [n for n in care.plants.names() if next_water(care, n) <= day]
    return sorted(names, key=lambda n: (next_water(care, n), n))


def alarm(temp):
    return temp < ALARM_BELOW


def overdue_days(care, name, day):
    return max(0, (day - next_water(care, name)).days)
