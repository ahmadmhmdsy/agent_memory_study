import csv


def write_csv(book, path):
    with open(path, "w", encoding="utf8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["name", "email", "phone"])
        for n in book.names():
            v = book.get(n)
            w.writerow([n, v["email"] or "", v["phone"] or ""])
        f.write(f"# {book.count()} contacts\n")
