import re


def clean_title(s):
    return " ".join(s.split())


def slug(title):
    return re.sub(r"[^a-z0-9-]", "", title.lower().replace(" ", "-"))
