"""Result lines and CSV export."""
import csv

from standings import points


def result_text(games, gid):
    w, b, r = games.get(gid)
    return f"{w} - {b}: {'draw' if r == '1/2' else r}"


def export_table(games, path):
    names = sorted(games.players.names(), key=lambda n: (-points(games, n), n))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "points", "rating"])
        for n in names:
            w.writerow([n, points(games, n), games.players.rating(n)])
