"""Points and standings."""

WIN = 3
DRAW = 1
PROVISIONAL = 8
FEE = 1800


def points(games, name):
    return games.wins(name) * WIN + games.draws(name) * DRAW


def is_provisional(games, name):
    return games.played(name) < PROVISIONAL


def entry_fee():
    return FEE


def table(games):
    return [(n, points(games, n)) for n in games.players.names()]
