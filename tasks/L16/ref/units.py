import re


def parse_duration(s):
    s = s.strip().lower()
    if ":" in s:
        h, m = s.split(":")
        v = int(h) * 60 + int(m)
    else:
        m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?", s)
        if not s or not m:
            raise ValueError("bad duration")
        v = int(m.group(1) or 0) * 60 + int(m.group(2) or 0)
    if not 1 <= v <= 300:
        raise ValueError("bad duration")
    return v
