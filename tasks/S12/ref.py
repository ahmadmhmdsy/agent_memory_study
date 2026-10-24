import csv


def row_total(row):
    return row["qty"] * row["price"]


def totals(rows):
    out = {}
    for r in rows:
        out[r["name"]] = out.get(r["name"], 0) + row_total(r)
    return out


def export(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["name", "qty", "price"])
        for r in rows:
            w.writerow([r["name"], r["qty"], r["price"]])
