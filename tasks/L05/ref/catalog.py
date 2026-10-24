import re


def normalize_isbn(s):
    d = re.sub(r"[-\s]", "", s)
    if not re.fullmatch(r"\d{13}", d):
        raise ValueError("bad ISBN")
    return d


class Catalog:
    def __init__(self):
        self.books = {}

    def add(self, isbn, title):
        self.books[isbn] = title

    def title(self, isbn):
        return self.books[isbn]


def search(catalog, word):
    w = word.lower()
    return sorted((i for i, t in catalog.books.items() if w in t.lower()), key=lambda i: (catalog.books[i], i))
