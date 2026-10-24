"""Library loans."""

LOAN_DAYS = 21


class Library:
    def __init__(self):
        self._title = {}
        self._out = {}

    def add_book(self, isbn, title):
        self._title[isbn] = title

    def lend(self, isbn, member, day):
        if isbn in self._out:
            raise ValueError("book is out")
        if len(self.held(member)) >= 3:
            raise ValueError("member holds 3 books")
        self._out[isbn] = (member, day)

    def is_out(self, isbn):
        return isbn in self._out

    def due(self, isbn):
        return self._out[isbn][1] + LOAN_DAYS

    def give_back(self, isbn):
        if isbn not in self._out:
            raise KeyError(isbn)
        del self._out[isbn]

    def held(self, member):
        return sorted(i for i, (m, _) in self._out.items() if m == member)

    def titles(self):
        return sorted(t for i, t in self._title.items() if i not in self._out)
