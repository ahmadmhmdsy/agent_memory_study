from cards import parse_tags

COLS = ["backlog", "todo", "doing", "done"]


class Board:
    def __init__(self):
        self.cols = {c: [] for c in COLS}
        self.titles = {}
        self._tags = {}
        self.n = 0

    @staticmethod
    def _clean(title):
        t = title.strip()
        if not t:
            raise ValueError("title required")
        return t

    def add(self, title):
        t = self._clean(title)
        self.n += 1
        self.titles[self.n] = t
        self.cols["backlog"].append(self.n)
        return self.n

    def where(self, cid):
        return next(c for c in COLS if cid in self.cols[c])

    def move(self, cid, column):
        if column not in self.cols:
            raise ValueError("unknown column")
        cur = self.where(cid)
        if cur == column:
            return
        if cur == "done":
            raise ValueError("card is done")
        if column == "doing" and len(self.cols["doing"]) >= 2:
            raise ValueError("doing is full")
        self.cols[cur].remove(cid)
        self.cols[column].append(cid)

    def column(self, name):
        return list(self.cols[name])

    def title(self, cid):
        return self.titles[cid]

    def rename(self, cid, title):
        self.titles[cid] = self._clean(title)

    def count(self):
        return sum(len(self.cols[c]) for c in COLS if c != "done")

    def tag(self, cid, s):
        self._tags[cid] = parse_tags(s)

    def tags(self, cid):
        return list(self._tags.get(cid, []))
