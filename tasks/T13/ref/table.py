"""League table."""


def standings(league):
    def gd(t):
        return sum(f - a for f, a in league.rows(t))
    return sorted(league.teams(), key=lambda t: (-league.points(t), -gd(t), t))
