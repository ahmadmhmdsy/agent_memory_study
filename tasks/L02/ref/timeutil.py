from datetime import datetime

FMT = "%Y-%m-%d %H:%M:%S"


def parse_ts(s):
    return datetime.strptime(s.replace("T", " "), FMT)


def fmt_ts(dt):
    return dt.strftime(FMT)


def fmt_minutes(n):
    h, m = divmod(n, 60)
    return " ".join(p for p in (f"{h}h" if h else "", f"{m}m" if m else "") if p) or "0m"


def is_weekend(s):
    return parse_ts(s).weekday() >= 5
