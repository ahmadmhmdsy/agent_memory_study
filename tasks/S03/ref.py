from datetime import date


def strip_all(items):
    return [s.strip() for s in items]


def split_fields(line):
    return [f.strip() for f in line.split(",")]


def parse_date_iso(s):
    try:
        return date.fromisoformat(s)
    except (ValueError, TypeError):
        return None
