from datetime import datetime

FMT = "%Y-%m-%d %H:%M:%S"


def parse_ts(s):
    return datetime.strptime(s.replace("T", " "), FMT)


def fmt_ts(dt):
    return dt.strftime(FMT)
