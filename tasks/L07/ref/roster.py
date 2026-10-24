import re


def initials(name):
    return "".join(p[0].upper() for p in re.split(r"[\s-]+", name.strip()) if p)
