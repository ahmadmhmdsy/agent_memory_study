import re


def is_valid_email(s):
    if s.count("@") != 1:
        return False
    a, b = s.split("@")
    return bool(a) and "." in b and not b.startswith(".")


def domain(email):
    return email.split("@", 1)[1].lower()


def _norm(name):
    return re.sub(r" +", ".", name.strip().lower())


class Users:
    def __init__(self):
        self._names = []

    def add(self, name):
        self._names.append(_norm(name))

    def names(self):
        return list(self._names)

    def has(self, name):
        return _norm(name) in self._names
