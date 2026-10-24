import re


def parse_plate(s):
    p = re.sub(r"[\s-]", "", s).upper()
    if not re.fullmatch(r"[A-Z0-9]{2,8}", p):
        raise ValueError("bad plate")
    return p
