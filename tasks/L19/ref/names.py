import re


def title_name(name):
    return " ".join("-".join(p.capitalize() for p in w.split("-")) for w in name.split())


def initials(name):
    return "".join(p[0].upper() for p in re.split(r"[\s-]+", name.strip()) if p)
