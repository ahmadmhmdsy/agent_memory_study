"""League results."""

WIN = 3


class League:
    def __init__(self):
        self._m = {}

    def record(self, home, away, home_goals, away_goals):
        if home == away:
            raise ValueError("a team cannot play itself")
        for g in (home_goals, away_goals):
            if not isinstance(g, int) or isinstance(g, bool) or g < 0:
                raise ValueError("goals are ints of 0 or more")
        self._m[(home, away)] = (home_goals, away_goals)

    def rows(self, team):
        for (h, a), (hg, ag) in self._m.items():
            if h == team:
                yield hg, ag
            elif a == team:
                yield ag, hg

    def points(self, team):
        return sum(WIN if f > a else 1 if f == a else 0 for f, a in self.rows(team))

    def teams(self):
        return sorted({t for k in self._m for t in k})

    def played(self, team):
        return sum(1 for _ in self.rows(team))

    def goals_for(self, team):
        return sum(f for f, _ in self.rows(team))
