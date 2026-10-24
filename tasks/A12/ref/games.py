"""Games."""

K = 24
FLOOR = 300


class Games:
    def __init__(self, players):
        self.players = players
        self._g = {}
        self._n = 0

    def record(self, white, black, result):
        self.players.rating(white)
        self.players.rating(black)
        if result not in ("1-0", "0-1", "1/2"):
            raise ValueError(f"bad result {result!r}")
        if white == black:
            raise ValueError("a player cannot play themselves")
        if sum({w, b} == {white, black} for w, b, _ in self._g.values()) >= 2:
            raise ValueError("these players have met twice")
        self._n += 1
        self._g[self._n] = (white, black, result)
        if result != "1/2":
            win, lose = (white, black) if result == "1-0" else (black, white)
            p = self.players
            p.set_rating(win, p.rating(win) + K)
            p.set_rating(lose, max(FLOOR, p.rating(lose) - K))
        return self._n

    def get(self, gid):
        return self._g[gid]

    def ids(self):
        return list(self._g)

    def count(self):
        return len(self._g)

    def last(self):
        return self._n if self._g else None

    def of_player(self, name):
        return [k for k, (w, b, _) in self._g.items() if name in (w, b)]

    def played(self, name):
        return len(self.of_player(name))

    def score(self, gid, name):
        w, b, r = self._g[gid]
        if r == "1/2":
            return "draw"
        return "win" if (r == "1-0") == (name == w) else "loss"

    def wins(self, name):
        return sum(self.score(k, name) == "win" for k in self.of_player(name))

    def losses(self, name):
        return sum(self.score(k, name) == "loss" for k in self.of_player(name))

    def draws(self, name):
        return sum(self.score(k, name) == "draw" for k in self.of_player(name))

    def opponents(self, name):
        return sorted({w if b == name else b for k in self.of_player(name) for w, b, _ in [self._g[k]]})
