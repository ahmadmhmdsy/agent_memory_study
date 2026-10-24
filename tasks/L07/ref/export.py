import csv
from stats import final_score, passed


def export_grades(book, path):
    rows = sorted(book.students(), key=lambda s: (-final_score(book, s), s))
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "final", "status"])
        for s in rows:
            w.writerow([s, final_score(book, s), "pass" if passed(book, s) else "fail"])
