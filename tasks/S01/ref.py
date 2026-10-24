from datetime import date, timedelta


def is_weekend(d):
    return d.weekday() >= 5


def weekday_name(d):
    return d.strftime("%A")


def next_business_day(d):
    d = d + timedelta(days=1)
    while d.weekday() >= 5:
        d += timedelta(days=1)
    return d.strftime("%d/%m/%Y")
