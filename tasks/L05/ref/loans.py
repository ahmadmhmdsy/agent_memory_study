import datetime as dt
import re
import unicodedata


def member_id(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"[^a-z0-9-]", "", s.replace(" ", "-"))


class Loans:
    def __init__(self):
        self.loans = {}

    def checkout(self, isbn, member, day):
        member = member.lower()
        if isbn in self.loans:
            raise ValueError("already on loan")
        if len(self.books_of(member)) >= 3:
            raise ValueError("too many loans")
        self.loans[isbn] = (member, day)

    def holder(self, isbn):
        return self.loans[isbn][0] if isbn in self.loans else None

    def books_of(self, member):
        return sorted(i for i, (m, _) in self.loans.items() if m == member.lower())

    def due(self, isbn):
        return self.loans[isbn][1] + dt.timedelta(days=21)

    def return_book(self, isbn, day):
        self.loans.pop(isbn, None)
