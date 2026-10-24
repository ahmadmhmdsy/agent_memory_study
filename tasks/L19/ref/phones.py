import re


def normalize_phone(s):
    p = re.sub(r"[\s().-]", "", s)
    if p.startswith("0"):
        p = "+49" + p[1:]
    return p


def check_email(e):
    if e is None:
        return None
    if e.count("@") != 1:
        raise ValueError("bad email")
    user, dom = e.split("@")
    if not user or "." not in dom:
        raise ValueError("bad email")
    return e
